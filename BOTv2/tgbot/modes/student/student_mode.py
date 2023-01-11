from datetime import datetime

from services.restapi.restapi import get_homework
from tgbot.entities.mode import Mode

from tgbot.modes.student.stages import *
from services.scripts import convert_homework


class StudentMode(Mode):
    STAGES = {
        "entry_stage": MenuStage,
        "choose_date": ChooseDate,
        "choose_subject": ChooseSubject,
        "send_hw": SendHwStage,
        "shedule": Schedule,
        "fast_add": FastChooseData,
        "get_hw_choose_date": GetHwChooseDate,
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
        if call.data == "menu":
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
        data = await get_homework(self.user.tgid, date)
        if isinstance(data, ApiError):
            # TODO: handle errors
            return
        print(data)
        # TODO: send homework
        await self.user.setup()