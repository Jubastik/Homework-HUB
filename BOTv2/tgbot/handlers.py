from aiogram.types import CallbackQuery, Message

from bot import dp, bot


@dp.callback_query_handler()
async def handle_start_query(call: CallbackQuery):
    await bot.um.handle_callback(call)


@dp.message_handler()
async def handle_start_query(msg: Message):
    await bot.um.handle_message(msg)
