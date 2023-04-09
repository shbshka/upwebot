import nest_asyncio
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram import types
import markups as nav
import random

from config import TOKEN
from global_f import randomizer, reset, set_card
from files import cards, vocabulary, cs, grammar, schedule
from cards import score_assigner, study_again, start_cards

nest_asyncio.apply()

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=storage)


# ----- Глобальные переменные -----
score = 0
i = 0
qs = []
cards_pool = []
n = -1
item = None
bad = []
try_again = []
good = []
awesome = []
scores, face_pool, back_pool, card = set_card(score, bad, try_again, good, awesome)


# ----- Стартовое сообщение -----
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(
        message.from_user.id, "Hello, {0.first_name}!".format(message.from_user), reply_markup=nav.mainMenu
    )


# ----- Регистрация (не работает) -----
class Registration(StatesGroup):

    name: State = State()
    surname: State = State()
    upwego_code: State = State()


@dp.message_handler(commands=["register"])
async def start_registration(message: types.Message):
    await message.answer("To start the registration process, set the following: ", reply_markup=nav.register)


@dp.message_handler(Text(equals="Enter name"))
async def process_set_name(message: types.Message):
    await Registration.name.set()
    await bot.send_message(message.from_user.id, "Enter your name, please")


@dp.message_handler(lambda message: message.text, content_types=[ContentType.TEXT], state=Registration.name)
async def load_name(message: types.Message, state: FSMContext):
    with state.proxy() as data:
        data["name"] = message.text

    await Registration.next()
    await message.reply("Name set successfully!")


@dp.message_handler(Text(equals="Enter surname"))
async def process_set_name(message: types.Message):
    await Registration.surname.set()
    await bot.send_message(message.from_user.id, "Enter your surname, please")


@dp.message_handler(lambda message: message.text, content_types=[ContentType.TEXT], state=Registration.surname)
async def load_name(message: types.Message, state: FSMContext):
    with state.proxy() as data:
        data["surname"] = message.text

    await state.finish()
    await message.answer("Surname set successfully!")


@dp.message_handler(Text(equals="Finish registration"))
async def finish_registration(message: types.Message):
    await bot.send_message(message.from_user.id, "Registration completed!", reply_markup=nav.mainMenu)


@dp.message_handler(Text(equals="Cancel"))
async def cancel_registration(message: types.Message, state: FSMContext):
    current_state = state.get_state()
    if current_state is None:
        return
    await bot.send_message(message.from_user.id, "Registration cancelled", reply_markup=nav.mainMenu)
    await state.finish()


# ----- Обработка reply markups -----
@dp.message_handler()
async def bot_message(message: types.Message):
    global qs
    global item
    global cards_pool

    if message.text == "View olympiad schedule":
        await bot.send_message(message.from_user.id, schedule["0"])

    if message.text == "Get tasks":
        await bot.send_message(
            message.from_user.id, "Choose the set of tasks to do.", reply_markup=nav.tasksMenu
         )

    if message.text == "Register with Upwego":
        await bot.send_message(
            message.from_user.id, "Press here: /register"
        )

    if message.text == "Vocabulary tasks":
        await reset()
        item = vocabulary
        qs = randomizer(item)
        await bot.send_message(
            message.from_user.id, "Press 'start' to begin the exercise.", reply_markup=nav.startTest
        )

    if message.text == "Main menu":
        await bot.send_message(
            message.from_user.id, "Returning to the main menu", reply_markup=nav.mainMenu
        )

    if message.text == "Grammar tasks":
        item = grammar
        qs = randomizer(item)
        await bot.send_message(
            message.from_user.id, "Press 'start' to begin the exercise.", reply_markup=nav.startTest
        )

    if message.text == "Country studies tasks":
        item = qs
        qs = randomizer(item)
        await bot.send_message(
            message.from_user.id, "Press 'start' to begin the exercise.", reply_markup=nav.startTest
        )

    if message.text == "Study cards":
        await bot.send_message(
            message.from_user.id, "Choose the set of cards to study.", reply_markup=nav.studyCards
        )

    if message.text == "Study existing cards":
        item = cards_pool
        cards_pool = randomizer(cards_pool)
        await bot.send_message(
            message.from_user.id, "Study cards?", reply_markup=nav.startCards
        )


# ----- Обработка ответов на задания -----
@dp.callback_query_handler(lambda call: True)
async def callback_handler(call: types.CallbackQuery):
    global score
    global qs
    global item
    global face_pool
    global back_pool
    global scores

    if call.data == "start_test":
        show_task = types.InlineKeyboardMarkup()
        await call.message.edit_reply_markup()
        try:
            q_num = qs.pop()
        except IndexError:
            await bot.send_message(
                call.from_user.id,
                f"Congratulations! You've completed all tasks! Your score: {score}.\nStart again? /start"
            )
            await reset()
        else:
            answers = item[q_num]["correct_answer"] + item[q_num]["incorrect_answer"]
            random.shuffle(answers)
            for answer in answers:
                if answer in item[q_num]["correct_answer"]:
                    good_answer = types.InlineKeyboardButton(text=str(answer), callback_data='correct')
                    show_task.add(good_answer)
                else:
                    bad_answer = types.InlineKeyboardButton(text=str(answer), callback_data="incorrect")
                    show_task.add(bad_answer)
            await bot.send_message(
                call.from_user.id, str(item[q_num]["question_text"]), reply_markup=show_task
            )

    if call.data == "correct":
        score += 1
        await bot.send_message(
            call.from_user.id, "Well done!", reply_markup=nav.ifQuit
        )
        await call.message.edit_reply_markup()

    if call.data == "incorrect":
        await bot.send_message(
            call.from_user.id, "Try again :(", reply_markup=nav.ifQuit
        )
        await call.message.edit_reply_markup()

    if call.data == "quit_test":
        await bot.send_message(
            call.from_user.id, f"Thank you for participation! Your score: {score}"
        )
        await call.message.edit_reply_markup()
        await reset()

# ---------------------------
# ----------- Cards ---------
# ---------------------------

    call_score = ["start_cards", "bad", "try_again", "good", "awesome"]

    if call.data in call_score:
        global n
        global cards_pool
        n += 1
        try:
            await bot.send_message(call.from_user.id, f"{face_pool[n]}", reply_markup=nav.show_answer)
        except IndexError:
            n = -1
            cards_pool = []
            await bot.send_message(call.from_user.id, "This is it for today!", reply_markup=nav.mainMenu)

    if call.data == "show_answer":
        await bot.send_message(call.from_user.id, f"{back_pool[n]}", reply_markup=nav.feedback)

    if call.data == "quit_cards":
        n = -1
        cards_pool = []
        await bot.send_message(call.from_user.id, "Thanks for studying!", reply_markup=nav.mainMenu)

    if call.data == "bad":
        score = 0
        study_again(scores, cards)

    if call.data == "try_again":
        score = 1
        study_again(scores, cards)

    if call.data == "good":
        score = 2
        study_again(scores, cards)

    if call.data == "awesome":
        score = 3
        study_again(scores, cards)

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
