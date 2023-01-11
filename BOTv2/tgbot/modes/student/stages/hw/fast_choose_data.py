from aiogram.types import CallbackQuery, Message
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import get_subjects_markup

from services.restapi import restapi
from services.restapi.api_error import ApiError


class FastChooseData(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = get_subjects_markup
        self.text = lambda *args, **kwargs: process_text(TextKeys.choose_subject, **kwargs)
    
    async def get_args(self) -> dict:
        subjects = await restapi.get_schedule(self.user.tgid, date=datetime.datetime.now().date())
        if isinstance(subjects, ApiError):
            # TODO: handle error
            return
        subjects_arg = list(set([i["lesson"]["name"] for i in subjects]))
        return {"markup_args": {"subjects": subjects_arg}, "text_args": {}}
        
    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "subject" in call.data:
            self.mode.set_subject(subject:=call.data.split(":")[1])
            date = await restapi.get_next_lesson_date(self.user.tgid, [subject])
            date = map(int, date[0]["date"].split("-"))
            date = datetime.date(*date)
            if isinstance(date, ApiError):
                # TODO: handle error
                return
            self.mode.set_add_date(date)
            await self.mode.set_stage("send_hw")
            return True