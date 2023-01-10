from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
)

from services.restapi.restapi import is_admin
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
