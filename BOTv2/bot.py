import os
import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.users_manager import UsersManager


bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=types.ParseMode.HTML)
bot.um = UsersManager()
dp = Dispatcher(bot, storage=MemoryStorage())
