from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.Filters.StudentFilter import StudentFilter

# Tasks:
# 1)

async def student_start(msg: Message):
    await msg.reply("Зареган")


def register_student_handlers(dp: Dispatcher):
    dp.register_message_handler(
        student_start, StudentFilter(), commands=["start"], state="*"
    )
