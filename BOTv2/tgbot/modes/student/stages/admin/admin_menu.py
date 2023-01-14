from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_class_panel,
)

from services.restapi.restapi import change_class_token, get_class, get_banned_users
from services.restapi.api_error import ApiError


class AdminMenu(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, status="", **kwargs: process_text(
            TextKeys.class_panel, status=status, **kwargs
        )
        self.markup = markup_class_panel

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "remove_token":
            users_class = await change_class_token(self.user.tgid)
            if isinstance(users_class, ApiError):
                # TODO
                pass
            await call.answer(
                process_text(TextKeys.token_changed, token=users_class["class_token"])
            )
            return True

        elif call.data == "add_admin":
            users_class = await get_class(self.user.tgid)
            if isinstance(users_class, ApiError):
                return users_class
            classmates = list(
                filter(
                    lambda student: student["is_admin"] is False
                    and student["tg_id"] != self.user.tgid,
                    users_class["student"],
                )
            )
            if len(classmates) == 0:
                await call.answer(process_text(TextKeys.no_assignable_admins))
                return True
            self.mode.get_stage("add_admin").set_classmates(classmates)
            await self.mode.set_stage("add_admin")
            return True

        elif call.data == "ban":
            users_class = await get_class(self.user.tgid)
            if isinstance(users_class, ApiError):
                return users_class
            classmates = list(
                filter(
                    lambda student: student["tg_id"] != self.user.tgid,
                    users_class["student"],
                )
            )
            if len(classmates) == 0:
                await call.answer(process_text(TextKeys.no_classmates_to_ban))
                return True
            self.mode.get_stage("ban_user").set_classmates(classmates)
            await self.mode.set_stage("ban_user")
            return True
        
        elif call.data == "unban":
            ban_list = await get_banned_users(self.user.tgid)
            if isinstance(ban_list, ApiError):
                return ban_list
            if len(ban_list) == 0:
                await call.answer(process_text(TextKeys.no_banned_users))
                return True
            self.mode.get_stage("unban_user").set_ban_list(ban_list)
            await self.mode.set_stage("unban_user")
            return True

        return False
