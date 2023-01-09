from tgbot.entities.stage import Stage

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
)

from services.restapi.restapi import is_admin
from services.restapi.api_error import ApiError

from bot import bot


class MenuStage(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.menu, **kwargs)
        self.markup = get_markup_student_menu

    async def get_args(self) -> dict:
        admin = await is_admin(self.user.tgid)
        if isinstance(admin, ApiError):
            await self.handle_api_error(admin)
            return admin
        return {"markup_args": {"is_admin": admin}, "text_args": {}}
