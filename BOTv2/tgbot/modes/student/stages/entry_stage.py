import asyncio
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
import datetime

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
)

from services.restapi.restapi import is_lessons_in_saturday, get_schedule, get_next_lesson_date, get_current_lessons
from services.restapi.api_error import ApiError
from services.scripts import get_seconds_to_event


class MenuStage(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, **kwargs: process_text(TextKeys.menu, **kwargs)
        self.markup = get_markup_student_menu
        self.update_func = None
        self.update_start_time = None
        self.update_end_time = None

    async def get_args(self) -> dict:
        subjects = await get_current_lessons(self.user.tgid)
        if isinstance(subjects, ApiError):
            return
        subjects = [subject["lesson"]["name"] for subject in subjects]
        return {"markup_args": {"subjects": subjects}, "text_args": {}}

    async def _prepare_args(self, markup_args={}, text_args={}, **kwargs):
        if self.update_func is None:
            await self.set_dynamic_update()

        res = await super()._prepare_args(markup_args, text_args, **kwargs)
        return res

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "add_on_date":
            await self.mode.set_stage("choose_date")
            return True
        elif call.data == "my_shedule":
            await self.mode.set_stage("shedule")
            return True
        elif call.data == "add_homework":
            if datetime.datetime.now().weekday() == 6:
                await call.answer("Сегодня нету уроков")
                return True
            await self.mode.set_stage("fast_add")
        elif call.data == "get_homework":
            await self.mode.set_stage("get_hw_choose_date")
            return True
        elif call.data == "get_next_date_hw":
            date = datetime.date.today() - datetime.timedelta(hours=4) + datetime.timedelta(days=1)
            if date.weekday() == 6:
                date += datetime.timedelta(days=1)
            elif date.weekday() == 5:
                suturday = await is_lessons_in_saturday(self.user.tgid)
                if isinstance(suturday, ApiError):
                    return
                if not suturday:
                    date += datetime.timedelta(days=2)
            await self.mode.send_homework(call, date)
            return True
        elif call.data == "profile":
            await self.mode.set_stage("profile")
            return True
        elif "subject" in call.data:
            self.mode.set_subject(subject := call.data.split(":")[1])
            date = await get_next_lesson_date(self.user.tgid, [subject])
            date = map(int, date[0]["date"].split("-"))
            date = datetime.date(*date)
            if isinstance(date, ApiError):
                # TODO: handle error
                return
            self.mode.set_add_date(date)
            await self.mode.set_stage("send_hw")
            return True
        return False

    async def set_dynamic_update(self):
        if self.update_func is not None:
            self.update_func.cancel()
        shedule = await get_schedule(self.user.tgid)
        shedule.sort(key=lambda x: x["slot"]["begin_time"])
        hours, minutes, seconds = map(int, shedule[0]["slot"]["begin_time"].split(":"))
        self.update_start_time = datetime.time(hours, minutes, seconds)
        self.update_end_time = datetime.time(hour=self.update_start_time.hour + 9)

        self.update_func = asyncio.create_task(self.dynamic_update())

    async def dynamic_update(self):
        print("dynamic update started")
        while True:
            # calculate time to next update
            now = datetime.datetime.now()
            if now.time() < self.update_start_time or now.time() > self.update_end_time:
                seconds_left = get_seconds_to_event(self.update_start_time + datetime.timedelta(minutes=1))
            else:
                i = 1
                while now.time < self.update_start_time + datetime.timedelta(hours=i):
                    i += 1
                seconds_left = get_seconds_to_event(self.update_start_time + datetime.timedelta(hours=i, minutes=1))

            await asyncio.sleep(seconds_left)
            try:
                await self.activate()
            except MessageNotModified:
                pass
