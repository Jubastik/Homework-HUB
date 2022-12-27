from aiogram.types import CallbackQuery, Message

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.handlers.registration.registration_stages import (
    StartStage,
    TimeStage,
    SubjectsStage,
    SheduleStage,
    JoinByIdStage,
)
from tgbot.keyboards.inline.markup import (
    get_markup_shedule,
    get_markup_student_menu,
    markup_check_subjects1,
    markup_shedule2,
    markup_start,
    markup_yes_or_no,
    markup_back,
)

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

    def check_data(self):
        pass

    def get_data(self):
        pass

    async def on_callback(self, call: CallbackQuery) -> None:
        cb_data = call.data
        if cb_data == "back":
            await self.stage_down(call=call)
        elif cb_data == "next":
            await self.stage_up(call=call)
        elif "change_stage:" in cb_data:
            stage = int(cb_data.split(":")[1])
            await self.change_stage(stage).on_callback(call)
        else:
            await self.stages[self.current_stage].on_callback(call)

    async def on_message(self, msg: Message) -> None:
        await self.stages[self.current_stage].on_message(msg)
