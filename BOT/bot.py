import os

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
