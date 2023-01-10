from aiogram.types import CallbackQuery, Message

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

    async def get_args(self) -> dict:
        date = self.mode.get_date().strftime("%d.%m.%Y")
        subject = self.mode.get_subject()
        return {"markup_args": {}, "text_args": {"date": date, "subject": subject}}

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "done":
            if self.hw_txt or self.hw_photos:
                print(self.hw_txt)
                print(self.hw_photos)
                # TODO: send homework to server
            else:
                await call.answer(process_text(TextKeys.no_hw, call))
            return True
        return False
    
    async def handle_message(self, msg: Message):
        if msg.text or msg.caption:
            self.hw_txt += msg.text or msg.caption
        if msg.photo:
            self.hw_photos.append(msg.photo[-1].file_id)
        return True