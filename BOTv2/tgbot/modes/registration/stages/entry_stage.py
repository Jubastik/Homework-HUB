from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import markup_start


class StartStage(Stage):
    name = "entry_stage"

    def __init__(self, mode) -> None:
        super().__init__(mode)
        self.markup = markup_start
        self.text = lambda *args, **kwargs: process_text(TextKeys.hello, **kwargs)
    
