from aiogram.types import CallbackQuery, Message
from asyncio import sleep

from tgbot.handlers.registration.stages.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_subjects_stage,
)
from CONSTANTS import SUBJECTS

from bot import bot


class SubjectsStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.subjects = SUBJECTS
        self.markup = markup_subjects_stage

    async def activate(self, call: CallbackQuery = None, status=""):
        subjects = "\n".join(self.subjects)
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(
                TextKeys.subjects_check,
                call,
                subjects=subjects,
                status=status,
            ),
            reply_markup=self.markup,
        )

    async def on_message(self, msg: Message):
        self.subjects += [msg.text]
        await self.activate()
        await sleep(1)
        await msg.delete()

    async def on_callback(self, call: CallbackQuery) -> bool:
        if call.data == "remove":
            self.subjects.pop()
            await self.activate()
            return True
        return False

    def get_subjects(self):
        return self.subjects
