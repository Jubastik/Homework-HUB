from aiogram import Dispatcher
from aiogram.types import Message

from bot import dp
from tgbot.Filters.AdminFilter import AdminFilter

# Tasks:
# 1) Изменение/удаление домашки в классе


@dp.message_handler(AdminFilter(), commands=["admin_panel"], state="*")
async def admin_panel(msg: Message):
    await msg.answer("Админка")
