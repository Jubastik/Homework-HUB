from aiogram.types import CallbackQuery
from datetime import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_menu,
)

from service.restapi import restapi
from service.restapi.api_error import ApiError
from CONSTANTS import WEEKDAYS_TO_NUM


class Schedule(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.empty, **kwargs)
        self.markup = markup_menu

    async def get_args(self) -> dict:
        schedule = await restapi.get_schedule(self.user.tgid)
        if isinstance(schedule, ApiError):
            # TODO: handle error
            pass
        days = []
        for lesson in schedule:
            if lesson["day"]["name"] not in days:
                days.append(lesson["day"]["name"])
        schedule_template = {i: {j: "" for j in range(1, 9)} for i in days}
        for lesson in schedule:
            schedule_template[lesson["day"]["name"]][lesson["slot"]["number_of_lesson"]] = lesson["lesson"]["name"]
        text = ""
        for day in schedule_template:
            text += f"<b>{day}:</b>\n"
            for lesson in schedule_template[day]:
                text += f"<code>{lesson})</code> {schedule_template[day][lesson]}\n"

        return {"markup_args": {}, "text_args": {"text": text}}
