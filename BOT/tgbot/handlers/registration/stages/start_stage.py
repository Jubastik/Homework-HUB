from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.handlers.registration.stages.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import markup_start

from bot import bot


class StartStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.markup = markup_start

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(TextKeys.hello, call, status=status),
            reply_markup=self.markup,
        )