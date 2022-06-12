import os
from pathlib import Path

from aiogram import Bot, types, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv

env_path = Path('..') / '.env'
load_dotenv(dotenv_path=env_path)

bot = Bot(token=os.getenv("TG_TOKEN"), parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
