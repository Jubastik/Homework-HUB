from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_shedule_stage,
)
from CONSTANTS import WEEKDAYS, WEEKDAYS_TRASNLATE, SUBJECTS

from bot import bot


class SheduleStage(Stage):
    name = "shedule_stage"

    def __init__(self, mode, day) -> None:
        super().__init__(mode)
        self.cur = 0
        self.day = day
        self.name = f"shedule_stage{day}"
        self.day_name = WEEKDAYS[day]
        self.day_tag = WEEKDAYS_TRASNLATE[self.day_name]
        self.shedule = [None] * 8
        self.markup = get_markup_shedule_stage
        self.max_len = 4  # max len of subject name. Default 4 because "1) -"

    async def activate(self, status=""):
        await bot.edit_message_text(
            chat_id=self.user.tgid,
            message_id=self.user.main_msg_id,
            text=process_text(
                TextKeys.shedule_stage,
                **self.get_text(),
                status=status,
            ),
            reply_markup=self.markup(SUBJECTS + self.mode.storage["subjects"]),
        )

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "up_or_down" in call.data:
            self.cur = (self.cur + int(call.data.split(":")[1])) % 8
            await self.activate()
            return True
        elif "subject" in call.data:
            self.shedule[self.cur] = call.data.split(":")[1]
            self.max_len = max(self.max_len, len(self.shedule[self.cur]))
            self.cur += 1
            await self.activate()
            return True
        elif call.data == "remove":
            self.shedule[self.cur] = None
            await self.activate()
            return True

    # returns day name and readable shedule
    def get_text(self):
        text = ""
        for i in range(8):
            if self.shedule[i] is not None:
                text += f"{i + 1}) {self.shedule[i]}"
            else:
                text += f"{i + 1}) -"
            if i == self.cur:
                text = text.ljust(self.max_len + 3) + "⬅️"
            text += "\n"
        return {
            "day_name": self.day_name,
            "shedule": text,
        }

    def get_shedule(self):
        return {
            "day_name": self.day_name,
            "day_tag": self.day_tag,
            "shedule": self.shedule,
        }


class LastSheduleStage(SheduleStage):
    def __init__(self, mode, day) -> None:
        super().__init__(mode, day)
        self.markup = lambda subjects: get_markup_shedule_stage(subjects, last_day=True)
