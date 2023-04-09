from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

btnMain = KeyboardButton(text='Main menu')

# ----- Main menu -----
btnSchedule = KeyboardButton(text='View olympiad schedule')
btnTasks = KeyboardButton(text='Get tasks')
btnRegister = KeyboardButton(text='Register with Upwego')
btnCards = KeyboardButton(text="Study cards")
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnTasks, btnSchedule, btnRegister, btnCards)

# ----- Tasks menu -----
btnVocabulary = KeyboardButton(text='Vocabulary tasks')
btnGrammar = KeyboardButton(text='Grammar tasks')
btnCS = KeyboardButton(text='Country studies tasks')
tasksMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnVocabulary, btnGrammar, btnCS, btnMain)

# ----- Task markups -----
btnStartTest = InlineKeyboardButton(text="Start", callback_data="start_test")
btnQuitTest = InlineKeyboardButton(text="Quit", callback_data="quit_test")
startTest = InlineKeyboardMarkup().add(btnStartTest, btnQuitTest)

btnContinue = InlineKeyboardButton(text='Continue?', callback_data='start_test')
btnQuit = InlineKeyboardButton(text='Quit', callback_data='quit_test')
ifQuit = InlineKeyboardMarkup().add(btnContinue, btnQuit)

# ----- Cards markups -----
btnNewCards = KeyboardButton(text="Add new card")
btnStudyCards = KeyboardButton(text="Study existing cards", callback_data="study_cards")
studyCards = ReplyKeyboardMarkup(resize_keyboard=True).add(btnNewCards, btnStudyCards, btnMain)

btnStartCards = InlineKeyboardButton(text="Start", callback_data="start_cards")
btnQuitCards = InlineKeyboardButton(text="Quit", callback_data="quit_cards")
startCards = InlineKeyboardMarkup().add(btnStartCards, btnQuitCards)

btnBad = InlineKeyboardButton(text="bad", callback_data="bad")
btnTryAgain = InlineKeyboardButton(text="try again", callback_data="try_again")
btnGood = InlineKeyboardButton(text="good", callback_data="good")
btnAwesome = InlineKeyboardButton(text="awesome", callback_data="awesome")
feedback = InlineKeyboardMarkup().add(btnBad, btnTryAgain, btnGood, btnAwesome, btnQuitCards)

btnAnswer = InlineKeyboardButton(text="Show answer", callback_data="show_answer")
show_answer = InlineKeyboardMarkup().add(btnAnswer)

# ----- Registration keyboard -----
btnSetName = KeyboardButton(text="Enter name")
btnSetSurname = KeyboardButton(text="Enter surname")
ifCancel = KeyboardButton(text="Cancel")
ifFinish = KeyboardButton(text="Finish registration")
register = ReplyKeyboardMarkup(resize_keyboard=True).add(btnSetName, btnSetSurname, ifFinish, ifCancel)