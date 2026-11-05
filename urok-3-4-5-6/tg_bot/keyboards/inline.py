from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def category_actions_kb(category_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton('изменить', callback_data=f'category_update:{category_id}'),
        InlineKeyboardButton('удалить', callback_data=f'category_delete:{category_id}'),
    )
    return kb


def product_actions_kb(product_id):
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton('изменить', callback_data=f'product_update:{product_id}'),
        InlineKeyboardButton('удалить', callback_data=f'product_delete:{product_id}'),  # product_delete:2
    )
    return kb


def product_update_kb(product_id):
    kb = InlineKeyboardMarkup()

    kb.add(
        InlineKeyboardButton(text='название', callback_data=f'update_product_name:{product_id}'),
        InlineKeyboardButton(text='количество', callback_data=f'update_product_quantity:{product_id}'),
        InlineKeyboardButton(text='стоимость', callback_data=f'update_product_price:{product_id}'),
        InlineKeyboardButton(text='категория', callback_data=f'update_product_category:{product_id}'),
    )
    return kb
