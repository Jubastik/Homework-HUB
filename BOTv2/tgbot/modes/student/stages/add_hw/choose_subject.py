from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import get_subjects_markup

from services.restapi import restapi
from services.restapi.api_error import ApiError


class ChooseSubject(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = get_subjects_markup
        self.text = lambda *args, **kwargs: process_text(TextKeys.choose_subject, **kwargs)

    async def get_args(self) -> dict:
        date = self.mode.get_date()
        subjects = await restapi.get_schedule(self.user.tgid, date)
        if isinstance(subjects, ApiError):
            await self.handle_api_error(subjects)
            return subjects
        subjects_arg = [i["lesson"]["name"] for i in subjects]
        return {"markup_args": {"subjects": subjects_arg}, "text_args": {}}
    
    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "subject:" in call.data:
            subject = call.data.split(":")[1]
            self.mode.set_subject(subject)
            await self.mode.set_stage("send_hw")
            return True
        return False
