from aiogram.types import CallbackQuery
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import get_markup_dates

from services.scripts import generate_dates
from services.restapi import restapi
from services.restapi.api_error import ApiError


class ChooseDate(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.date = None
        self.markup = get_markup_dates
        self.text = lambda *args, **kwargs: process_text(TextKeys.choose_date, **kwargs)

    async def get_args(self) -> dict:
        dates = await restapi.is_lessons_in_saturday(self.user.tgid)
        if isinstance(dates, ApiError):
            await self.handle_api_error(dates)
            return dates
        dates = generate_dates(dates)
        return {"markup_args": {"dates": dates}, "text_args": {}}

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "add_date:" in call.data:
            year, month, day = map(int, call.data.split(":")[1].split("-"))
            self.date = datetime.date(year, month, day)
            self.mode.set_date(self.date)
            await self.mode.set_stage("choose_subject")
            return True
        return False

    def get_date(self) -> datetime.date:
        return self.date
