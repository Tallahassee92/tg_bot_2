
from settings.loader import config
from tg_bot.loader import bot
from tg_bot.handlers import admin, user
from database.managers.base import table_manager

def main():
    table_manager.create_tables()

    print(table_manager.manage('select * from categories;', fetchall=True))
    bot.infinity_polling()



main()


