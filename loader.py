from telebot import TeleBot, custom_filters
from config import TOKEN
from telebot.storage import StateMemoryStorage
from telebot.types import BotCommand
from database.database import DataBase

bot = TeleBot(TOKEN, state_storage=StateMemoryStorage())

db = DataBase()

bot.add_custom_filter(custom_filters.StateFilter(bot))

bot.set_my_commands(commands=[
    BotCommand('start', 'reload the bot'),
    BotCommand('help', 'for help')
])



