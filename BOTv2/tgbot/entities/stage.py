from aiogram.types import CallbackQuery, Message

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
import logging


class Stage:  # Abstract class
    name = "entry_stage"

    def __init__(self, mode):
        self.mode = mode
        self.user = mode.user

    async def handle_callback(self, call: CallbackQuery) -> bool:
        await call.answer()
        return False

    async def handle_message(self, msg: Message):
        # Обработка неожидаемых сообщений
        return False

    async def activate(self, **kwargs):
        logging.warning(f"{type(self)} have no activate() method")
