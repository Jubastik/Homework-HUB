from aiogram.types import CallbackQuery, Message, User

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.handlers.registration.stages import (
    JoinByIdStage,
    StartStage,
    TimeStage,
    SubjectsStage,
    SheduleStage,
)
from tgbot.keyboards.inline.markup import markup_start, get_markup_student_menu
from tgbot.services.restapi.restapi import register_class, is_admin, get_student_info
from tgbot.services.scripts import make_username
from tgbot.services.sub_classes import RestErorr
from tgbot.FSM.states import StudentMenu
from CONSTANTS import TG_OFFICAL_CHANNEL, TG_BOT_LINK


from bot import dp


class RegistrationManager:  # О ДААА! НОРМАЛЬНЫЙ ООП КОД
    def __init__(self, start_msg: Message) -> None:
        # dont forget to call init_registration() after creating this object
        self.userid = start_msg.from_user.id
        self.current_stage = 1
        self.FSMContext = dp.current_state(user=self.userid)
        self.stages = [
            JoinByIdStage(self),
            StartStage(self),
            TimeStage(self),
            SubjectsStage(self),
            SheduleStage(self, 0),
            SheduleStage(self, 1),
            SheduleStage(self, 2),
            SheduleStage(self, 3),
            SheduleStage(self, 4),
            SheduleStage(self, 5),
        ]

    async def init_registration(self, msg):  # to start you have to call this method
        new_message = await msg.answer(
            process_text(TextKeys.hello, msg, status=""), reply_markup=markup_start
        )
        self.main_message_id = new_message.message_id

    async def change_stage(self, stage: int):
        self.current_stage = stage
        return self.stages[self.current_stage]

    async def stage_up(self, call=None):
        self.current_stage += 1
        if call is not None:
            await self.stages[self.current_stage].activate(call)
        return self.stages[self.current_stage]

    async def stage_down(self, call=None):
        self.current_stage -= 1
        if call is not None:
            await self.stages[self.current_stage].activate(call)
        return self.stages[self.current_stage]

    async def register(self, call):
        data = self.get_data()
        res = await register_class(self.userid, data)
        if isinstance(res, RestErorr):
            await call.answer(res.error_message)
            return
        return "registered"


    def get_data(self):
        start_time = self.stages[2].get_time()
        username = make_username(User.get_current())
        shedule = {}
        for i in range(4, 10):
            shedule[i] = self.stages[i].get_shedule()
        return {
            "start_time": start_time,
            "shedule": shedule,
            "subjects": self.get_subjects(),
            "username": username,
        }

    async def on_callback(self, call: CallbackQuery) -> None:
        cb_data = call.data
        if await self.stages[self.current_stage].on_callback(call):
            return True
        elif cb_data == "back":
            await self.stage_down(call=call)
        elif cb_data == "next":
            await self.stage_up(call=call)
        elif "change_stage:" in cb_data:
            stage = int(cb_data.split(":")[1])
            await self.change_stage(stage).on_callback(call)
        elif cb_data == "register":
            res = await self.register(call)
            return res
        else:
            return False
        return True

    async def on_message(self, msg: Message) -> None:
        await self.stages[self.current_stage].on_message(msg)

    def get_subjects(self):
        return self.stages[3].get_subjects()
