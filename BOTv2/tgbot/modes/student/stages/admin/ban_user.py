from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_classmates,
)

from services.restapi.restapi import get_class, ban_user
from services.restapi.api_error import ApiError


class BanUser(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, status="", **kwargs: process_text(
            TextKeys.choose_classmate, status=status, **kwargs
        )
        self.markup = get_markup_classmates
        self.classmates = None

    def set_classmates(self, classmates):
        self.classmates = classmates

    async def get_args(self):
        if self.classmates is None:
            users_class = await get_class(self.user.tgid)
            if isinstance(users_class, ApiError):
                return users_class
            classmates = list(
                filter(
                    lambda student: student["tg_id"] != self.user.tgid,
                    users_class["student"],
                )
            )
        else:
            classmates = self.classmates
        return {"markup_args": {"data": classmates}, "text_args": {}}

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if "student_name:" in call.data:
            tgid = int(call.data.split(":")[1])
            name = call.data.split(":")[2]
            res = await ban_user(tgid)
            if isinstance(res, ApiError):
                # TODO
                return res
            await call.answer(process_text(TextKeys.user_banned, name=name))
            await self.mode.set_stage("admin_menu")
            return True
        return False
