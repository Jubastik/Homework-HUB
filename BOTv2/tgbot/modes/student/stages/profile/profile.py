from aiogram.types import CallbackQuery
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_profile,
)

from services.restapi.restapi import get_user, get_class
from services.restapi.api_error import ApiError


class Profile(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.profile, **kwargs)
        self.markup = markup_profile
    
    async def get_args(self) -> dict:
        user = await get_user(self.user.tgid)
        if isinstance(user, ApiError):
            return
        users_class = await get_class(self.user.tgid)
        if isinstance(users_class, ApiError):
            return
        admins = []
        for student in users_class["student"]:
            if student["is_admin"]:
                admins.append(student["name"])
        admins = " ".join(admins)        
    
        text_args = {
            "name": user["name"],
            "is_admin": "✅" if user["is_admin"] else "❌",
            "class_token": users_class["class_token"],
            "admins": admins
        }

        return {"markup_args": {"is_admin": user["is_admin"]}, "text_args": text_args}