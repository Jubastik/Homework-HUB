from aiogram.types import Message

from bot import bot, dp


@dp.message_handler(
    state="*",
    commands=["menu", "get_hw", "get_homework", "start"],
)
async def menu(msg: Message):
    await msg.answer("Mailings in development. Coming soon.")