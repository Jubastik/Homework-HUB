from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.handlers.registration.stages.stage import Stage
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
from tgbot.FSM.states import RegistrationStates, StudentMenu
from tgbot.services.restapi.restapi import (
    get_student_info,
    is_admin,
    register_class,
    register_user,
)
from tgbot.services.scripts import convert_time, make_username, time_is_correct
from CONSTANTS import SUBJECTS, WEEKDAYS
from tgbot.services.sub_classes import RestErorr

from bot import bot


class TimeStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.time = time(hour=9, minute=0)
        self.markup = markup_registration_default

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(
                TextKeys.start_time_check,
                call,
                time=self.time.strftime("%H:%M"),
                status=status,
            ),
            reply_markup=self.markup,
        )

    async def on_message(self, msg: Message):
        if time_is_correct(msg.text):
            self.time = convert_time(msg.text)
            await self.activate(
                msg, status=process_text(TextKeys.status_time_changed, msg)
            )
            await sleep(1)
            await msg.delete()
        else:
            await self.activate(msg, status=process_text(TextKeys.wrong_time, msg))
            await sleep(1)
            await msg.delete()
    
    def get_time(self):
        return self.time