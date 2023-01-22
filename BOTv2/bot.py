import locale
import os

import aiohttp
import cloudpickle
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.users_manager import UsersManager

# Set's Russian locale for datetime
locale.setlocale(locale.LC_ALL, "ru_RU.UTF-8")

bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=types.ParseMode.HTML)
try:
    with open("um.pcl", "rb") as f:
        bot.um = cloudpickle.load(f)
except FileNotFoundError:
    print("FileNotFoundError: um.pcl")
    bot.um = UsersManager()
except Exception as e:
    print("Unexpected error")
    print(e)
    bot.um = UsersManager()
dp = Dispatcher(bot, storage=MemoryStorage())

headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}
session = aiohttp.ClientSession(headers=headers)
