from asyncio import sleep
from aiogram.types import User

from tgbot.entities.mode import Mode

from tgbot.modes.registration import *

from services.restapi.api_error import ApiError
from services.restapi import restapi
from services.scripts import make_username


class RegistrationMode(Mode):
    STAGES = {
        "join_by_id_stage": JoinByIdStage,
        "entry_stage": StartStage,
        "time_stage": TimeStage,
        "subjects_stage": SubjectsStage,
        "shedule_stage0": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=0),
        "shedule_stage1": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=1),
        "shedule_stage2": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=2),
        "shedule_stage3": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=3),
        "shedule_stage4": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=4),
        "shedule_stage5": lambda *args, **kwargs: LastSheduleStage(*args, **kwargs, day=5),
    }
    STAGES_NUM_TO_NAME = {i: name for i, name in enumerate(STAGES)}
    STAGES_NAME_TO_NUM = {name: i for i, name in enumerate(STAGES)}
    STAGES_LEN = len(STAGES)

    async def handle_callback(self, call) -> bool:
        handled = await self.current_stage.handle_callback(call) if self.current_stage else False
        if handled:
            return True
        elif call.data == "back":
            num = self.STAGES_NAME_TO_NUM[self.current_stage.name] - 1
            await self.set_stage(num)
            return True
        elif call.data == "next":
            num = self.STAGES_NAME_TO_NUM[self.current_stage.name] + 1
            await self.set_stage(num)
            return True
        elif call.data == "register":
            await self.register(call)
            return True
        return False
    
    async def handle_message(self, msg) -> bool:
        handled = await self.current_stage.handle_message(msg) if self.current_stage else False
        if handled or isinstance(handled, ApiError):
            return True
        return False
    
    def get_subjects(self):
        if self.stages["subjects_stage"]:
            return self.stages["subjects_stage"].get_subjects()
        return []
    
    def get_time(self):
        if self.stages["time_stage"]:
            return self.stages["time_stage"].get_time()
        return None

    async def register(self, call):
        class_name = make_username(User.get_current())
        shedule = []
        for i in range(6):
            if f"shedule_stage{i}" in self.stages:
                shedule += self.stages[f"shedule_stage{i}"].get_shedule()
        print("SHEDULE:", shedule)
        print("tg_id:", self.user.tgid)
        print("class_name:", class_name)
        print("start_time:", self.get_time())
        await restapi.create_class(tg_id=self.user.tgid, class_name=class_name, shedule=shedule, start_time=self.get_time())
        await self.user.setup()