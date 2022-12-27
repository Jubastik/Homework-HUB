from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from datetime import time
import logging
from tgbot.keyboards.inline.markup import (
    markup_start,
    markup_registration_default,
    markup_join_by_id_stage,
    get_markup_student_menu,
)
from tgbot.FSM.states import RegistrationStates, StudentMenu
from tgbot.services.restapi.restapi import (
    get_student_info,
    is_admin,
    register_class,
    register_user,
)
from tgbot.services.scripts import convert_time, make_username, time_is_correct
from CONSTANTS import SUBJECTS
from tgbot.services.sub_classes import RestErorr

from bot import bot


class Stage:  # Abstract class
    async def activate(self, call: CallbackQuery):
        logging.warning(f"{type(self)} have no activate() method")

    async def get_data(self, msg: Message):
        logging.warning(f"{type(self)} have no get_data() method")

    async def on_callback(self, call: CallbackQuery):
        await call.answer()
        logging.warning(f"{type(self)} have no on_callback() method; CallbackQuery: {call.data}")

    async def on_message(self, msg: Message):
        # Обработка неожидаемых сообщений
        await self.activate(status=process_text(TextKeys.unexpected_message, msg))
        await sleep(1)
        await msg.delete()

    async def activate(self, **kwargs):
        logging.warning(f"{type(self)} have no activate() method")


class StartStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.markup = markup_start

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(TextKeys.hello, call, status=status),
            reply_markup=self.markup,
        )


class JoinByIdStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.markup = markup_join_by_id_stage

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(TextKeys.get_class_token, call, status=status),
            reply_markup=self.markup,
        )
        await call.answer()

    async def on_message(self, msg: Message):
        classid = msg.text
        if classid.isdigit():
            username = make_username(User.get_current())
            res = await register_user(self.rm.userid, classid, username)
            if isinstance(res, RestErorr):
                await self.activate(status="something went wrong, try again")
                await sleep(1)
                await msg.delete()
                return
            print("await self.rm.registred()")
            # await self.rm.registred()
            await self.rm.FSMContext.reset_state()
            await StudentMenu.Menu.set()
            res = await is_admin(msg.from_user.id)
            if isinstance(res, RestErorr):
                return
            await msg.answer(
                process_text(TextKeys.menu, msg),
                reply_markup=get_markup_student_menu(res),
            )
        else:
            await self.activate(status=process_text(TextKeys.wrong_class_token, msg))
            await sleep(1)
            await msg.delete()


class TimeStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.time = time(hour=9, minute=0)
        self.markup = markup_registration_default

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(
                TextKeys.start_time_check,
                call,
                time=self.time.strftime("%H:%M"),
                status=status,
            ),
            reply_markup=self.markup,
        )

    async def on_message(self, msg: Message):
        if time_is_correct(msg.text):
            self.time = convert_time(msg.text)
            await self.activate(msg, status=process_text(TextKeys.status_time_changed, msg))
            await sleep(1)
            await msg.delete()
        else:
            await self.activate(msg, status=process_text(TextKeys.wrong_time, msg))
            await sleep(1)
            await msg.delete()


class SubjectsStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.subjects = SUBJECTS
        self.markup = markup_registration_default
    
    async def activate(self, call: CallbackQuery = None, status=""):
        subjects = "\n".join(self.subjects)
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(
                TextKeys.subjects_check,
                call,
                subjects=subjects,
                status=status,
            ),
            reply_markup=self.markup,
        )


class SheduleStage(Stage):
    def __init__(self, rm, day) -> None:
        self.rm = rm
        self.day = day
