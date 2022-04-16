from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.filters.student_filter import StudentFilter


@dp.message_handler(StudentFilter(), commands=["start", "menu"], state="*")
async def student_menu(msg: Message):
    await msg.answer("Какая-то менюшка")
