from aiogram import Bot, Dispatcher, executor
import json
from aiogram import types
import markups as nav
import random

TOKEN = "5262008776:AAHeEOyHn8O97K2WhjApMM6MX0LWthmw7lo"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


# ----- Файлы для работы -----
with open("./vocabulary.json", "r") as f_voc:
    vocabulary = json.load(f_voc)
with open("schedule.json", "rb") as f_sch:
    schedule = json.load(f_sch)
with open ("./grammar.json", "r") as f_gram:
    grammar = json.load(f_gram)

# ----- Глобальные переменные -----
score = 0
i = 0
qs = []
task = None


# ----- Глобальные функции -----
def randomizer(task):
    key = [str(x) for x in range(len(task))]
    random.shuffle(key)
    return key


async def reset():
    global score
    global qs
    score = 0
    qs = []


# ----- Стартовое сообщение -----
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await reset()
    await bot.send_message(
        message.from_user.id, "Hello, {0.first_name}".format(message.from_user), reply_markup=nav.mainMenu
    )


# ----- Обработка reply markups -----
@dp.message_handler()
async def bot_message(message: types.Message):
    global qs
    global task

    if message.text == "View olympiad schedule":
        await bot.send_message(message.from_user.id, schedule["0"])

    if message.text == "Get tasks":
        await bot.send_message(
            message.from_user.id, "Choose the set of tasks to do.", reply_markup=nav.tasksMenu
         )

    if message.text == "Vocabulary tasks":
        task = vocabulary
        qs = randomizer(task)
        await bot.send_message(
            message.from_user.id, "Press 'start' to begin the exercise.", reply_markup=nav.startTest
        )

    if message.text == "Main menu":
        await bot.send_message(
            message.from_user.id, "Returning to the main menu", reply_markup=nav.mainMenu
        )

    if message.text == "Grammar tasks":
        task = grammar
        qs = randomizer(task)
        await bot.send_message(
            message.from_user.id, "Press 'start' to begin the exercise.", reply_markup=nav.startTest
        )


# ----- Обработка ответов на задания -----
@dp.callback_query_handler(lambda call: True)
async def task_handler(call: types.CallbackQuery):
    global score
    global qs
    global task

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
            answers = task[q_num]["correct_answer"] + task[q_num]["incorrect_answer"]
            random.shuffle(answers)
            for answer in answers:
                if answer in task[q_num]["correct_answer"]:
                    good_answer = types.InlineKeyboardButton(text=str(answer), callback_data='correct')
                    show_task.add(good_answer)
                else:
                    bad_answer = types.InlineKeyboardButton(text=str(answer), callback_data="incorrect")
                    show_task.add(bad_answer)
            await bot.send_message(
                call.from_user.id, str(task[q_num]["question_text"]), reply_markup=show_task
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



if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
