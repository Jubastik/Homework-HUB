from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_next,
    markup_register_done2,
    markup_join_done,
)

from aiogram.types import CallbackQuery


class RegisterDoneStage1(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = markup_next
        self.text = lambda *args, **kwargs: process_text(
            TextKeys.register_done1, **kwargs
        )

    async def get_args(self) -> dict:
        return {
            "markup_args": {},
            "text_args": {"token": self.mode.students_class["class_token"]},
        }

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "next":
            await self.mode.set_stage("register_done2")
            return True
        return False


class RegisterDoneStage2(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = markup_register_done2
        self.text = lambda *args, **kwargs: process_text(
            TextKeys.register_done2, **kwargs
        )

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "next":
            await self.user.setup()
            return True
        elif call.data == "connect_diary":
            await self.mode.set_stage("spb_diary_get_login")
            return True
        return False


class JoinRegisterDone(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = markup_join_done
        self.text = lambda *args, **kwargs: process_text(
            TextKeys.join_register_done, **kwargs
        )

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "next":
            await self.user.setup()
            return True
        return False
