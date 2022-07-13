from aiogram.types import Message

from bot import dp
from languages.text_proccesor import process_text
from languages.text_keys import TextKeys

@dp.message_handler(commands=["help"], state="*")
async def hanldler_start(msg: Message):
    await msg.answer(process_text(TextKeys.help_txt, msg))