from aiogram.types import CallbackQuery, Message
from asyncio import sleep

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_subjects_stage,
)
from CONSTANTS import SUBJECTS

from bot import bot


class SubjectsStage(Stage):
    name = "subjects_stage"

    def __init__(self, mode) -> None:
        super().__init__(mode)
        self.subjects = []
        self.markup = markup_subjects_stage
        self.text = lambda *args, **kwargs: process_text(TextKeys.subjects_check, **kwargs)

    async def get_args(self) -> dict:
        return {"text_args": {"subjects": "\n".join(SUBJECTS + self.subjects), "status": ""}, "markup_args": {}}

    async def handle_message(self, msg: Message):
        self.subjects += [msg.text]
        await self.activate(text_args={"status": process_text(TextKeys.status_subject_added, msg)})
        await sleep(1)
        await msg.delete()
        return True

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "remove":
            if self.subjects:
                self.subjects.pop()
                await self.activate()
            else:
                pass
                # TODO: send message that there is no subjects to remove
            return True
        return False

    def get_subjects(self):
        return self.subjects
