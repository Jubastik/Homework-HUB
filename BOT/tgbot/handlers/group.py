from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.filters.group_filter import GroupFilter


@dp.message_handler(GroupFilter(), state="*")
async def dev_panel(msg: Message):
    await msg.answer("channel /start answer")
    await msg.answer(f"INFO ABOUT CHAT: {msg.chat}")