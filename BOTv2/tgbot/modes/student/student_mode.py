import asyncio
from aiogram.types import InputMediaPhoto
from datetime import datetime

from services.restapi.restapi import get_homework, get_parsed_hw
from tgbot.entities.mode import Mode

from tgbot.modes.student.stages import *
from tgbot.modes.common_stages.spb_diary import SPBDiaryGetLogin, SPBDiaryGetPassword
from services.scripts import convert_homework, delete_msg



class StudentMode(Mode):
    STAGES = {
        "entry_stage": MenuStage,
        "choose_date": ChooseDate,
        "choose_subject": ChooseSubject,
        "send_hw": SendHwStage,
        "shedule": Schedule,
        "fast_add": FastChooseData,
        "get_hw_choose_date": GetHwChooseDate,
        "profile": Profile,
        "hw_history": HwHistoryChooseDate,
        "delete_account": DeleteAccount,
        "admin_menu": AdminMenu,
        "add_admin": AddAdmin,
        "ban_user": BanUser,
        "unban_user": UnbanUser,
        "spb_diary_get_login": SPBDiaryGetLogin,
        "spb_diary_get_password": SPBDiaryGetPassword,
    }
    STAGES_NUM_TO_NAME = {i: name for i, name in enumerate(STAGES)}
    STAGES_NAME_TO_NUM = {name: i for i, name in enumerate(STAGES)}
    STAGES_LEN = len(STAGES)

    def __init__(self, user):
        super().__init__(user)
        self.add_date = None
        self.subject = None

    async def handle_callback(self, call) -> bool:
        handled = await self.current_stage.handle_callback(call)
        if handled:
            return True
        if call.data == "menu" or call.data == "back":
            self.__init__(self.user)
            await self.set_stage("entry_stage")
            return True
        return False

    async def handle_message(self, msg) -> bool:
        handled = await self.current_stage.handle_message(msg) if self.current_stage else False
        if handled:
            return True
        return False

    def get_add_date(self) -> datetime.date:
        return self.add_date

    def set_add_date(self, date: datetime.date):
        self.add_date = date

    def get_subject(self) -> str:
        return self.subject

    def set_subject(self, subject):
        self.subject = subject

    async def send_homework(self, call: CallbackQuery, date: datetime.date):
        # Getting and converting homework
        data_hw = await get_homework(self.user.tgid, date)
        if isinstance(data_hw, ApiError):
            # TODO: handle errors
            return
        diary_hw = await get_parsed_hw(self.user.tgid, date)
        if isinstance(diary_hw, ApiError):
            if diary_hw.error_code == 1501 or diary_hw.error_code == 1502:
                diary_hw = None
            else:
                return
        info_msg = await call.message.answer(f"Домашка на {date.strftime('%A %d.%m')}👇🏻")
        asyncio.create_task(delete_msg(info_msg, 600))
        homeworks = convert_homework(data_hw, call, diary_hw)
        # Sending homework
        if len(homeworks) == 0:
            await call.answer(f"На {date.strftime('%A %d.%m')} нет домашнего задания❌")
            if self.stage_num != self.STAGES_NAME_TO_NUM["entry_stage"]:
                await self.set_stage("entry_stage")
            return
        for lesson in homeworks:
            if len(lesson["photos"]) != 0:
                media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
                for photo in lesson["photos"][1:]:
                    media.append(InputMediaPhoto(photo))
                msg = await call.message.answer_media_group(media, disable_notification=True)
                for m in msg:
                    asyncio.create_task(delete_msg(m, 600))
            else:
                msg = await call.message.answer(lesson["text"], disable_notification=True)
                asyncio.create_task(delete_msg(msg, 600))
        await self.user.reset()
    
    async def register_diary(self, login: str, password: str):
        res = await restapi.create_parser(self.user.tgid, login, password)
        await self.set_stage("profile")
        if isinstance(res, ApiError):
            return res