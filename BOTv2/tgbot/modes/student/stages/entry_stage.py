import asyncio
from aiogram.types import CallbackQuery
from aiogram.utils.exceptions import MessageNotModified
import datetime
from random import randint

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
        data = await get_current_lessons(self.user.tgid)
        if isinstance(data, ApiError):
            return
        # set(list()) to remove duplicates
        data = [subject["lesson"]["name"] for subject in data]
        subjects = sorted(set(data), key=lambda x: data.index(x))  # sorted by indexes in original data
        print(f"tgid:{self.user.tgid} current subjects - {subjects}")
        return {"markup_args": {"subjects": subjects}, "text_args": {}}

    async def _prepare_args(self, markup_args={}, text_args={}, **kwargs):
        if self.update_func is None:
            await self.set_dynamic_update()

        res = await super()._prepare_args(markup_args, text_args, **kwargs)
        return res

    async def handle_callback(self, call: CallbackQuery) -> bool:
        if call.data == "add_on_date":
            self.update_func.cancel()
            self.update_func = None
            await self.mode.set_stage("choose_date")
            return True
        elif call.data == "my_shedule":
            self.update_func.cancel()
            self.update_func = None
            await self.mode.set_stage("shedule")
            return True
        elif call.data == "add_homework":
            if datetime.datetime.now().weekday() == 6:
                await call.answer("Сегодня нету уроков")
                return True
            self.update_func.cancel()
            self.update_func = None
            await self.mode.set_stage("fast_add")
        elif call.data == "get_homework":
            self.update_func.cancel()
            self.update_func = None
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
            self.update_func.cancel()
            self.update_func = None
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
            self.update_func.cancel()
            self.update_func = None
            await self.mode.set_stage("send_hw")
            return True
        return False

    async def set_dynamic_update(self):
        if self.update_func is not None:
            self.update_func.cancel()
        shedule = await get_schedule(self.user.tgid)
        shedule.sort(key=lambda x: x["slot"]["begin_time"])
        hours, minutes, seconds = map(int, shedule[0]["slot"]["begin_time"].split(":"))
        if minutes < 11:
            minutes += 60
            hours -= 1
        self.update_start_time = datetime.time(hours, minutes - 11, seconds)
        self.update_end_time = datetime.time(hour=self.update_start_time.hour + 10, minute=0)
        self.update_func = asyncio.create_task(self.dynamic_update())

    async def dynamic_update(self):
        while True:
            # calculate time to next update
            now = datetime.datetime.now()
            if now.time() < self.update_start_time or now.time() > self.update_end_time:
                seconds_left = get_seconds_to_event(self.update_start_time)
            else:
                i = 1
                while now.time() > datetime.time(
                    hour=self.update_start_time.hour + i, minute=self.update_start_time.minute + 1
                ):
                    i += 1
                seconds_left = get_seconds_to_event(
                    datetime.time(hour=self.update_start_time.hour + i, minute=self.update_start_time.minute + 1)
                )
            seconds_left += randint(0, 60)
            print(f"dynamic update will be in {seconds_left} seconds, now is {now.time()}, it will be at {now + datetime.timedelta(seconds=seconds_left)}")
            await asyncio.sleep(seconds_left + 5)
            if self.mode.current_stage != self:
                self.update_func = None
                break
            try:
                await self.mode.set_stage("entry_stage")
            except MessageNotModified:
                # message was not modified, so we don't need to update it, just continue
                self.update_func = None
                break