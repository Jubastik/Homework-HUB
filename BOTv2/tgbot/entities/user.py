from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
from asyncio import sleep

from tgbot.entities.mode import Mode
from services.restapi import restapi
from services.restapi.api_error import ApiError

from tgbot.modes.registration.registration_mode import RegistrationMode
from tgbot.modes.student.student_mode import StudentMode


class User:
    MODES = {
        "registration_mode": RegistrationMode,
        "student_mode": StudentMode,
    }

    def __init__(self, um, tgid: int, main_msg_id: int = None):
        self.tgid = tgid
        self.um = um
        self.main_msg_id = main_msg_id
        self.mode = None
        # TODO: language

    async def setup(self, mode: Mode = None) -> None:
        if mode is not None:
            self.mode = mode
        else:
            is_student = await restapi.is_student(self.tgid)
            if isinstance(is_student, ApiError):
                await self.handle_api_error(is_student)
                return is_student
            if is_student:
                self.mode = self.MODES["student_mode"](self)
            else:
                self.mode = self.MODES["registration_mode"](self)
        if self.main_msg_id:
            await self.mode.set_stage("entry_stage")
        else:
            self.main_msg_id = await self.mode.send_entry()

    async def reset(self, mode: Mode = None) -> None:
        await self.delete_main_msg()
        await self.setup(mode)

    async def change_mode(self, mode: str) -> None:
        self.mode = self.MODES[mode](self)
        await self.mode.set_stage("entry_stage")

    async def delete_main_msg(self) -> None:
        from bot import bot

        if self.main_msg_id is not None:
            try:
                await bot.delete_message(self.tgid, self.main_msg_id)
            except (MessageCantBeDeleted, MessageToDeleteNotFound):
                pass
            self.main_msg_id = None

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if not self.mode:
            await self.reset()
        handled = await self.mode.handle_callback(call)
        return handled

    async def handle_message(self, msg: Message) -> bool:
        if msg.text and "/start" in msg.text:
            await self.reset()
            if self.mode is None or isinstance(self.mode, self.MODES["registration_mode"]):
                txt = msg.text.split()
                if len(txt) == 2 and txt[1].isdigit():
                    await self.mode.join_class(int(txt[1].replace("class_token", "")))
            await sleep(0.5)
            await msg.delete()
            return True
        if not self.mode:
            await self.reset()
        handled = await self.mode.handle_message(msg)
        return handled

    async def handle_api_error(self, error) -> bool:
        return False
