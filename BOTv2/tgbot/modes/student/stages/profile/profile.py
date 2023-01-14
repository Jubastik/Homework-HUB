from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_profile,
)

from services.restapi.restapi import get_user, get_class, get_parser_status, delete_parser
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
        pstatus = await get_parser_status(self.user.tgid)
        if isinstance(pstatus, ApiError):
            # TODO:
            return
        if pstatus == 0:
            parser_status = "не подключен❌"
        elif pstatus == 1:
            parser_status = "подключен✅"
        else:
            parser_status = "ошибка⚠️"
        admins = []
        for student in users_class["student"]:
            if student["is_admin"]:
                admins.append(student["name"])
        admins = " ".join(admins)        
    
        text_args = {
            "name": user["name"],
            "is_admin": "✅" if user["is_admin"] else "❌",
            "class_token": users_class["class_token"],
            "admins": admins,
            "parser_status": parser_status,
        }

        return {"markup_args": {"is_admin": user["is_admin"], "parser_status": pstatus}, "text_args": text_args}
    
    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "get_homework_history":
            await self.mode.set_stage("hw_history")
            return True
        elif call.data == "delete_account":
            await self.mode.set_stage("delete_account")
            return True
        elif call.data == "class_management":
            await self.mode.set_stage("admin_menu")
            return True
        elif call.data == "connect_spb_diary":
            await self.mode.set_stage("spb_diary_get_login")
            return True
        elif call.data == "disable_spb_diary":
            await delete_parser(self.user.tgid)
            await call.answer("Парсер отключен🫡")
            await self.mode.set_stage("profile")
        return False