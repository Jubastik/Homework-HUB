from asyncio import sleep
from aiogram.types import User

from tgbot.entities.mode import Mode

from tgbot.modes.registration import *
from tgbot.modes.common_stages.spb_diary import SPBDiaryGetLogin, SPBDiaryGetPassword

from services.restapi.api_error import ApiError
from services.restapi import restapi
from services.scripts import make_username

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


class RegistrationMode(Mode):
    tasks = []
    STAGES = {
        "join_by_id_done": JoinRegisterDone,
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
        "register_done1": RegisterDoneStage1,
        "register_done2": RegisterDoneStage2,
        "spb_diary_get_login": SPBDiaryGetLogin,
        "spb_diary_get_password": SPBDiaryGetPassword,
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
    
    async def join_class(self, class_token):
        from bot import bot

        username = make_username(User.get_current())
        user = await restapi.create_user(self.user.tgid, username, int(class_token))
        if isinstance(user, ApiError):
            if user.error_code == 1102:
                warning = await bot.send_message(self.user.tgid, process_text(TextKeys.u_are_banned))
                await sleep(3)
                await warning.delete()
            elif user.error_code == 1202:
                warning = await bot.send_message(self.user.tgid, process_text(TextKeys.class_not_found))
                await sleep(3)
                await warning.delete()
            return ApiError
        await self.set_stage("join_by_id_done")

    async def register(self, call):
        class_name = make_username(User.get_current())
        shedule = []
        for i in range(6):
            if f"shedule_stage{i}" in self.stages:
                shedule += self.stages[f"shedule_stage{i}"].get_shedule()
        await restapi.create_user(tg_id=self.user.tgid, name=class_name)
        self.students_class = await restapi.create_class(tg_id=self.user.tgid, class_name=class_name, schedules=shedule, start_time=self.get_time())
        await self.set_stage("register_done1")

    async def register_diary(self, login: str, password: str):
        res = await restapi.create_parser(self.user.tgid, login, password)
        if isinstance(res, ApiError):
            if res.error_code == 1502:
                await self.set_stage("register_done2")
            return res
        await self.user.setup()