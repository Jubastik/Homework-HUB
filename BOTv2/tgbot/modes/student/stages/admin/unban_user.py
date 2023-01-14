from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_banned_users,
)

from services.restapi.restapi import get_banned_users, unban_user
from services.restapi.api_error import ApiError


class UnbanUser(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, status="", **kwargs: process_text(
            TextKeys.choose_classmate, status=status, **kwargs
        )
        self.markup = get_markup_banned_users
        self.ban_list = None

    def set_ban_list(self, ban_list):
        self.ban_list = ban_list

    async def get_args(self):
        if self.ban_list is None:
            ban_list = await get_banned_users(self.user.tgid)
            if isinstance(ban_list, ApiError):
                return ban_list
        else:
            ban_list = self.ban_list
        return {"markup_args": {"data": ban_list}, "text_args": {}}

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "student_name:" in call.data:
            ban_id = int(call.data.split(":")[1])
            print(ban_id)
            name = call.data.split(":")[2]
            res = await unban_user(ban_id)
            if isinstance(res, ApiError):
                # TODO
                return res
            await call.answer(process_text(TextKeys.user_unbanned, name=name))
            await self.mode.set_stage("admin_menu")
            return True
        return False
