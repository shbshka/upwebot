from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnMain = KeyboardButton(text='Main menu')

# ----- Main menu -----
btnSchedule = KeyboardButton(text='View olympiad schedule')
btnTasks = KeyboardButton(text='Get tasks')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTasks, btnSchedule)

# ----- Tasks menu -----
btnVocabulary = KeyboardButton(text='Vocabulary tasks')
btnGrammar = KeyboardButton(text='Grammar tasks')
btnCS = KeyboardButton(text='Country studies tasks')
tasksMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnVocabulary, btnGrammar, btnCS, btnMain)

# ----- Task markups -----
btnStart = InlineKeyboardButton(text="start", callback_data="start_test")
startTest = InlineKeyboardMarkup().add(btnStart)

btnContinue = InlineKeyboardButton(text='Continue?', callback_data='start_test')
btnQuit = InlineKeyboardButton(text='Quit', callback_data='quit_test')
ifQuit = InlineKeyboardMarkup().add(btnContinue, btnQuit)