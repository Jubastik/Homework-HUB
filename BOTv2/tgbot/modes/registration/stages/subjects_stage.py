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
        self.mode.storage["subjects"] = self.mode.storage.get("subjects", [])
        self.markup = markup_subjects_stage
        self.text = lambda status="": process_text(
            TextKeys.subjects_check,
            subjects="\n".join(SUBJECTS + self.mode.storage["subjects"]),
            status=status,
        )

    async def handle_message(self, msg: Message):
        self.mode.storage["subjects"] += [msg.text]
        await self.activate()
        await sleep(1)
        await msg.delete()
        return True

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "remove":
            if self.mode.storage["subjects"]:
                self.mode.storage["subjects"].pop()
                await self.activate()
            else:
                pass
                # TODO: send message that there is no subjects to remove
            return True
        return False
