from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.Filters.AdminFilter import AdminFilter

# Tasks:
# 1) Изменение/удаление домашки в классе


async def admin_panel(msg: Message):
    await msg.reply("Админка")


def register_admin_handlers(dp: Dispatcher):
    dp.register_message_handler(
        admin_panel, AdminFilter(), commands=["admin_panel"], state="*"
    )
