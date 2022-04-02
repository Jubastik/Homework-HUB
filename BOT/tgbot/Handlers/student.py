from aiogram import Dispatcher
from aiogram.types import Message

from bot import dp
from tgbot.Filters.StudentFilter import StudentFilter


@dp.message_handler(StudentFilter(), commands=["start"], state="*")
async def student_start(msg: Message):
    await msg.answer("Зареган")
