from aiogram.types import CallbackQuery
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
)

from services.restapi.restapi import is_lessons_in_saturday
from services.restapi.api_error import ApiError


class MenuStage(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.menu, **kwargs)
        self.markup = get_markup_student_menu
    
    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "add_on_date":
            await self.mode.set_stage("choose_date")
            return True
        elif call.data == "my_shedule":
            await self.mode.set_stage("shedule")
            return True
        elif call.data == "add_homework":
            await self.mode.set_stage("fast_add")
        elif call.data == "get_homework":
            await self.mode.set_stage("get_hw_choose_date")
            return True
        elif call.data == "get_next_date_hw":
            date = datetime.date.today() - datetime.timedelta(hours=4) + datetime.timedelta(days=1)
            if date.weekday() == 6:
                date += datetime.timedelta(days=1)
            elif date.weekday() == 5:
                suturday = await is_lessons_in_saturday(self.user.tgid)
                if isinstance(suturday, ApiError):
                    return
                if not suturday:
                    date += datetime.timedelta(days=2)
            await self.mode.send_homework(call, date)
            return True
        elif call.data == "profile":
            await self.mode.set_stage("profile")
            return True
        return False
