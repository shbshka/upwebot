import nest_asyncio
import aioschedule
import logging
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types.message import ContentType
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ParseMode
from aiogram import types
import markups as nav
import random

from config import TOKEN
from global_f import randomizer, reset, set_card
from files import cards, vocabulary, cs, grammar, schedule, registred_users
from cards import score_assigner, study_again, start_cards
from registration import User

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

# -----------------------
# ----- Регистрация -----
# -----------------------

class Registration(StatesGroup):
    name = State()
    surname = State()
    upwego_code = State()

@dp.message_handler(commands=["register"])
async def assing_variables(message: types.Message):
    await bot.send_message(message.from_user.id, "Enter your name", reply_markup=nav.registration)
    await Registration.name.set()


@dp.message_handler(state="*", commands=["cancel"])
@dp.message_handler(Text(equals="Cancel registration"), state="*")
async def cancel_registration(message: types.Message, state: FSMContext):
    await state.finish()
    await message.reply("Registration cancelled", reply_markup=nav.mainMenu)

@dp.message_handler(state=Registration.name)
async def process_get_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["name"] = message.text
    await Registration.next()
    await message.reply("Enter your surname")

@dp.message_handler(state=Registration.surname)
async def process_get_surname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["surname"] = message.text
    await Registration.next()
    await message.reply("Enter your Upwego code")

@dp.message_handler(state=Registration.upwego_code)
async def process_get_code(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["upwego_code"] = message.text

    await bot.send_message(message.chat.id, md.text(
        md.text("Your name: ", md.bold(data["name"])),
        md.text("Your surname: ", md.bold(data["surname"])),
        md.text("Your Upwego code: ", md.bold(data["upwego_code"])),
            sep="\n",
            ),
        reply_markup=nav.mainMenu,
        parse_mode=ParseMode.MARKDOWN
        )

    await state.finish()

# -----------------------------------
# ----- Обработка reply markups -----
#------------------------------------

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

    if message.text == "Cancel registration":
        await bot.send_message(message.from_user.id, "Press here: /cancel")

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
        item = cs
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

    if message.text == "Add a new card":
        await bot.send_message(message.from_user.id, "In modification :(")


#-----------------------------------------
# ----- Обработка ответов на задания -----
#-----------------------------------------
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
                f"Congratulations! You've completed all tasks! Your score: {score}.", reply_markup=nav.mainMenu
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
            call.from_user.id, f"Thank you for participation! Your score: {score}", reply_markup=nav.mainMenu
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
