from aiogram.types import CallbackQuery, Message, ContentType

from bot import dp, bot


@dp.callback_query_handler()
async def handle_start_query(call: CallbackQuery):
    if call.message.chat["type"] == "group":
        # TODO: groups manager
        return
    await bot.um.handle_callback(call)


@dp.message_handler(content_types=ContentType.ANY)
async def handle_start_query(msg: Message):
    if msg.chat["type"] == "group":
        # TODO: groups manager
        return
    await bot.um.handle_message(msg)
