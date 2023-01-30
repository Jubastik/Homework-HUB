from asyncio import sleep
from aiogram.types import Message


from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

from tgbot.keyboards.inline.markup import markup_back

from services.restapi.api_error import ApiError


class SPBDiaryGetPassword(Stage):
    name = "spb_diary_get_password"
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.spb_diary_get_password)
        self.markup = markup_back
    
    async def handle_message(self, msg: Message):
        login = self.mode.get_stage("spb_diary_get_login").get_login()
        res = await self.mode.register_diary(login, msg.text)
        if isinstance(res, ApiError):
            if res.error_code == 1502:
                info_msg = await msg.answer("Неверный логин или пароль")
                await sleep(1)
                await msg.delete()
                await sleep(2)
                await info_msg.delete()
                return True
            else:
                info_msg = await msg.answer("Внутренняя ошибка Электронного дневника❌\nВ данный момент подключение Петербургского Образования невозможно😭")
                await sleep(1)
                await msg.delete()
                await sleep(2)
                await info_msg.delete()
                return True
        info_msg = await msg.answer('"Петербургское Образование" подключено🥳')
        await sleep(1)
        await msg.delete()
        await sleep(1)
        await info_msg.delete()
        return True