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
if os.getenv("LOAD_CACHE") == "True":
    try:
        with open("um.pcl", "rb") as f:
            bot.um = cloudpickle.load(f)
        print("um.pcl file loaded successfully")
    except FileNotFoundError:
        print("FileNotFoundError: um.pcl")
        print("Starting without um.cpl file...")
        bot.um = UsersManager()
    except Exception as e:
        print("Unexpected error while init um.cpl file:", e)
        print("Starting without um.cpl file...")
        bot.um = UsersManager()
else:
    bot.um = UsersManager()
    print("Starting without um.cpl file...")
dp = Dispatcher(bot, storage=MemoryStorage())

headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}
session = aiohttp.ClientSession(headers=headers)
