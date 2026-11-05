from tg_bot.loader import bot
from telebot import types


@bot.message_handler(commands=['start'], is_admin=False)
def user_start(message: types.Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'hello, user')
