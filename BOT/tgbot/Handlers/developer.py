from aiogram import Dispatcher
from aiogram.types import Message

from tgbot.Filters.DeveloperFilter import DeveloperFilter


async def dev_panel(msg: Message):
    await msg.reply("Developer panel")


def register_developer_handlers(dp: Dispatcher):
    dp.register_message_handler(
        dev_panel, DeveloperFilter(), commands=["dev_panel"], state="*"
    )
