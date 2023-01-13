from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_class_panel,
)

from services.restapi.restapi import change_class_token
from services.restapi.api_error import ApiError


class AdminMenu(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, status="", **kwargs: process_text(TextKeys.class_panel, status=status, **kwargs)
        self.markup = markup_class_panel

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "remove_token":
            users_class = await change_class_token(self.user.tgid)
            if isinstance(users_class, ApiError):
                # TODO
                pass
            await call.answer(process_text(TextKeys.token_changed, token=users_class["class_token"]))
