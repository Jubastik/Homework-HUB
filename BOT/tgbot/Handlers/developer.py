from aiogram import Dispatcher
from aiogram.types import Message

from bot import dp
from tgbot.Filters.DeveloperFilter import DeveloperFilter

# Tasks:
# 1) Создание рассылок


@dp.message_handler(DeveloperFilter(), commands=["dev_panel"], state="*")
async def dev_panel(msg: Message):
    await msg.answer("Developer panel")
