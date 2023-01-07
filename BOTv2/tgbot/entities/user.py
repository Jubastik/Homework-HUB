from aiogram.types import Message, CallbackQuery

from tgbot.entities.mode import Mode


class User:
    def __init__(self, um, tgid: int, main_msg_id: int = None):
        self.tgid = tgid
        self.um = um
        self.main_msg_id = main_msg_id
        # TODO: language

    def set_mode(self, mode: Mode) -> None:
        self.mode = mode
    
    def set_main_msg_id(self, msg_id: int) -> None:
        self.main_msg_id = msg_id

    async def handle_callback(self, call: CallbackQuery) -> bool:
        return await self.mode.handle_callback(call)

    async def handle_message(self, msg: Message) -> bool:
        return await self.mode.handle_message(msg)

    def handle_api_error(self, error) -> bool:
        return False
