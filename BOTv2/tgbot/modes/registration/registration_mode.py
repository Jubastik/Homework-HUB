from asyncio import sleep

from tgbot.entities.mode import Mode

from tgbot.modes.registration import *


class RegistrationMode(Mode):
    STAGES = {
        "entry_stage": EntryStage,
        "join_by_id_stage": JoinByIdStage,
        # "time_stage": TimeStage,
        # "subjects_stage": SubjectsStage,
        # "shedule_stage0": lambda *args, **kwargs: FirstSheduleStage(*args, **kwargs, day=0),
        # "shedule_stage1": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=1),
        # "shedule_stage2": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=2),
        # "shedule_stage3": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=3),
        # "shedule_stage4": lambda *args, **kwargs: SheduleStage(*args, **kwargs, day=4),
        # "shedule_stage5": lambda *args, **kwargs: LastSheduleStage(*args, **kwargs, day=5),
    }
    STAGES_NUM_TO_NAME = {
        1: "entry_stage",
        0: "join_by_id_stage",
        # 2: "time_stage",
        # 3: "subjects_stage",
        # 4: "shedule_stage0",
        # 5: "shedule_stage1",
        # 6: "shedule_stage2",
        # 7: "shedule_stage3",
        # 8: "shedule_stage4",
        # 9: "shedule_stage5",
    }
    STAGES_NAME_TO_NUM = {
        "entry_stage": 1,
        "join_by_id_stage": 0,
        # "time_stage": 2,
        # "subjects_stage": 3,
        # "shedule_stage0": 4,
        # "shedule_stage1": 5,
        # "shedule_stage2": 6,
        # "shedule_stage3": 7,
        # "shedule_stage4": 8,
        # "shedule_stage5": 9,
    }

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
            pass
        return False
    
    async def handle_message(self, msg) -> bool:
        if msg.text == "/start":
            msg_id = await self.set_stage("entry_stage")
            self.user.set_main_msg_id(msg_id)
            await sleep(0.5)
            await msg.delete()
            return True
        handled = await self.current_stage.handle_message(msg) if self.current_stage else False
        if handled:
            return True
        return False

    async def register(self, call):
        pass
