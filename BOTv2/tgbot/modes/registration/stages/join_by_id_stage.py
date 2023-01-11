from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_join_by_id_stage)
from services.scripts import make_username
from services.restapi.restapi import create_user
from services.restapi.api_error import ApiError


class JoinByIdStage(Stage):
    name = "join_by_id_stage"

    def __init__(self, mode) -> None:
        super().__init__(mode)
        self.markup = lambda *args, **kwargs: markup_join_by_id_stage
        self.text = lambda *args, **kwargs: process_text(TextKeys.get_class_token, status=kwargs.get("status", ""))

    async def handle_message(self, msg: Message) -> bool:
        classid = msg.text
        if classid.isdigit():
            username = make_username(User.get_current())
            user = await create_user(self.user.tgid, username, classid)
            if isinstance(user, ApiError):
                await self.handle_api_error(user)
                return ApiError
            await self.user.change_mode("student_mode")
        else:
            await self.activate(status=process_text(TextKeys.wrong_class_token, msg))
            await sleep(1)
        await msg.delete()
        return True
