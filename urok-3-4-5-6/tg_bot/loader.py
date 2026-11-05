import logging

import telebot
from telebot import TeleBot

from settings.loader import config
from .filters import IsAdmin

from telebot.states.sync import StateMiddleware
from telebot.custom_filters import StateFilter
from telebot.storage import StateMemoryStorage

# .message_handler(state=)
# IsAdmin() - is_admin=

# INFO, DEBUG, INFO

telebot.logger.setLevel(logging.DEBUG)

bot = TeleBot(config.bot.token, parse_mode='HTML',
              state_storage=StateMemoryStorage(),
              use_class_middlewares=True)
bot.add_custom_filter(IsAdmin())
bot.setup_middleware(StateMiddleware(bot))
bot.add_custom_filter(StateFilter(bot))


