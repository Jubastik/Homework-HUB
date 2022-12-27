from aiogram.types import Message

from bot import bot, dp
from tgbot.filters.group_filter import GroupFilter


@dp.message_handler(
    GroupFilter(),
    state="*",
    commands=["menu", "get_hw", "get_homework", "start"],
)
async def menu(msg: Message):
    await msg.answer("Group mailings in development. Coming soon.")
