from asyncio import sleep
from aiogram.types import Message

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import markup_back


class SPBDiaryGetLogin(Stage):
    name = "spb_diary_get_login"

    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.spb_diary_get_login)
        self.markup = markup_back
        self.login = None
    
    async def handle_message(self, msg: Message):
        self.login = msg.text
        await self.mode.set_stage("spb_diary_get_password")
        await sleep(1)
        await msg.delete()
        return True
    
    def get_login(self):
        return self.login