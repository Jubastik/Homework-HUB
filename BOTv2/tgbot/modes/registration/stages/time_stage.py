from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from datetime import time
import logging
from tgbot.keyboards.inline.markup import (
    markup_start,
    markup_registration_default,
    markup_join_by_id_stage,
    get_markup_student_menu,
    markup_subjects_stage,
    get_markup_shedule_stage,
)
from services.scripts import convert_time, make_username, time_is_correct
from CONSTANTS import SUBJECTS, WEEKDAYS
from services.sub_classes import RestErorr

from bot import bot


class TimeStage(Stage):
    name = "time_stage"

    def __init__(self, mode) -> None:
        super().__init__(mode)
        self.time = time(hour=9, minute=0)
        self.markup = markup_registration_default
        self.text = lambda *args, **kwargs: process_text(
            TextKeys.start_time_check,
            **kwargs,
        )

    async def get_args(self) -> dict:
        return {"text_args": {"time": self.time.strftime("%H:%M"), "status": ""}, "markup_args": {}}

    async def handle_message(self, msg: Message):
        if time_is_correct(msg.text):
            self.time = convert_time(msg.text)
            await self.activate(text_args={"status": process_text(TextKeys.status_time_changed, msg)})
            await sleep(1)
            await msg.delete()
        else:
            await self.activate(text_args={"status": process_text(TextKeys.wrong_time, msg)})
            await sleep(1)
            await msg.delete()
        return True

    def get_time(self):
        return self.time
