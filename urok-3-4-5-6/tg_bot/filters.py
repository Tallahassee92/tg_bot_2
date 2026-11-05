from settings.loader import config

from telebot import custom_filters


class IsAdmin(custom_filters.SimpleCustomFilter):
    key = 'is_admin'

    @staticmethod
    def check(message):
        return message.chat.id in config.bot.admin_ids