from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.Filters.RegistrationFilter import RegistrationFilter

# Tasks:
# 1) Регистрация
# 2) Присоединение
# 3) Обработка фаст ссылок

async def user_start(msg: Message):
    await msg.reply("Незареган")


def register_registration_handlers(dp: Dispatcher):
    dp.register_message_handler(
        user_start, RegistrationFilter(), commands=["start"], state="*"
    )
