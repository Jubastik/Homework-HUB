from aiogram.types import CallbackQuery, Message
from asyncio import sleep

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
import logging


class Stage:  # Abstract class
    async def on_callback(self, call: CallbackQuery) -> bool:
        await call.answer()
        return False

    async def on_message(self, msg: Message):
        # Обработка неожидаемых сообщений
        await self.activate(status=process_text(TextKeys.unexpected_message, msg))
        await sleep(1)
        await msg.delete()

    async def activate(self, **kwargs):
        logging.warning(f"{type(self)} have no activate() method")
