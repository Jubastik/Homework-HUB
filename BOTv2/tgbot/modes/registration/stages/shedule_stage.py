from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_shedule_stage,
)
from CONSTANTS import WEEKDAYS, WEEKDAYS_TRASNLATE, SUBJECTS


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
        self.text = lambda *args, **kwargs: process_text(TextKeys.shedule_stage, **kwargs)
        self.max_len = 4  # max len of subject name. Default 4 because "1) -"
    
    async def get_args(self) -> dict:
        return {"text_args": {**self.get_text()}, "markup_args": {"subjects": SUBJECTS + self.mode.get_subjects()}}

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

    def get_shedule(self) -> list:
        shedule = []
        for i in range(len(self.shedule)):
            if self.shedule[i] is not None:
                shedule.append({
                    "lesson": self.shedule[i],
                    "day_of_week": self.day_name,
                    "lesson_number": i + 1,
                })
        return shedule


class LastSheduleStage(SheduleStage):
    def __init__(self, mode, day) -> None:
        super().__init__(mode, day)
        self.markup = lambda subjects: get_markup_shedule_stage(subjects, last_day=True)
