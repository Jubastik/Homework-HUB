import os
import locale

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.users_manager import UsersManager


# Set's Russian locale for datetime
locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=types.ParseMode.HTML)
bot.um = UsersManager()
dp = Dispatcher(bot, storage=MemoryStorage())
