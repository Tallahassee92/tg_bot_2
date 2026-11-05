from telebot.types import ReplyKeyboardMarkup, KeyboardButton


def admin_kb():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton('категории'),
        KeyboardButton('продукты'),
        KeyboardButton('пользователи')
    )
    return kb


def admin_actions_kb(user_action = False):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(
        KeyboardButton('добавить'),
        KeyboardButton('получить'),
    )
    if user_action:
        kb.keyboard[0].pop(0)
    return kb


def categories_kb(categories):
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    for i in categories:
        kb.add(KeyboardButton(i.get('title')))
    return kb
