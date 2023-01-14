from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_are_u_sure,
)

from services.restapi.restapi import delete_user
from services.restapi.api_error import ApiError


class DeleteAccount(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.delete_account, **kwargs)
        self.markup = markup_are_u_sure

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "true":
            await delete_user(self.user.tgid)
            await self.user.reset()
            return True
        return False