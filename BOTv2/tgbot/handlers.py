import datetime

from aiogram.types import CallbackQuery, Message, ContentType
from sentry_sdk import Hub, start_transaction

from bot import dp, bot


@dp.callback_query_handler()
async def handle_start_query(call: CallbackQuery):
    with start_transaction(op="task", name="callback"):
        if call.message.chat["type"] == "private":
            await bot.um.handle_callback(call)
        # TODO: groups manager



@dp.message_handler(content_types=ContentType.ANY)
async def handle_start_query(msg: Message):
    with start_transaction(op="task", name="massage"):
        if msg.chat["type"] == "private":
            await bot.um.handle_message(msg)
    # TODO: groups manager
