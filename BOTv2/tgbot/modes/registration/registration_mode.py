from asyncio import sleep

from tgbot.entities.mode import Mode

from tgbot.modes.registration import *


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
            return True
        return False
    
    async def handle_message(self, msg) -> bool:
        if msg.text == "/start":
            msg_id = await self.reset()
            self.user.set_main_msg_id(msg_id)
            await sleep(0.5)
            await msg.delete()
            return True
        handled = await self.current_stage.handle_message(msg) if self.current_stage else False
        if handled:
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
        pass
