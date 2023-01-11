from aiogram.types import CallbackQuery, Message
from aiogram.utils.exceptions import MessageToDeleteNotFound
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import markup_done

from services.restapi import restapi
from services.restapi.api_error import ApiError


class SendHwStage(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.markup = markup_done
        self.text = lambda *args, **kwargs: process_text(TextKeys.send_homework, **kwargs)
        self.hw_txt = ""
        self.hw_photos = []
        self.messages = []  # messages_id to delete

    async def get_args(self) -> dict:
        date = self.mode.get_add_date().strftime("%A %d.%m").capitalize()
        subject = self.mode.get_subject()
        return {"markup_args": {}, "text_args": {"date": date, "subject": subject}}

    async def handle_callback(self, call: CallbackQuery) -> bool:
        from bot import bot

        if call.data == "done":
            if self.hw_txt or self.hw_photos:
                print(self.hw_photos)
                subject = self.mode.get_subject()
                date = self.mode.get_add_date()
                for i in self.messages:
                    try:
                        await bot.delete_message(self.user.tgid, i)
                    except MessageToDeleteNotFound:
                        pass
                created = await restapi.create_homework(self.user.tgid, subject, date, self.hw_txt, self.hw_photos)
                if isinstance(created, ApiError):
                    pass
                    # TODO: handle error
                date = created["date"].split("-")
                date = datetime.date(year=int(date[0]), month=int(date[1]), day=int(date[2]))
                subject = created["schedule"]["lesson"]["name"]
                await call.answer(f"⚡️Записано на {date.strftime('%A %d.%m')} {subject}")
                await self.user.setup()
            else:
                await call.answer(process_text(TextKeys.no_hw, call))
            return True
        return False

    async def handle_message(self, msg: Message):
        self.messages += [msg.message_id]
        if msg.text or msg.caption:
            self.hw_txt += msg.text or msg.caption
        if msg.photo:
            self.hw_photos.append(msg.photo[-1].file_id)
        return True
