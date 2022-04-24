from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
import datetime

from BOT.bot import dp
from BOT.tgbot.FSM.states import (
    StudentAddHomework,
    StudentProfile,
    StudentMenu,
    StudentGetHomework,
    StudentClass,
)
from BOT.tgbot.filters.student_filter import StudentFilter
from BOT.tgbot.filters.admin_filter import AdminFilter
from BOT.tgbot.services.scripts import generate_dates
from BOT.tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    get_markup_fast_add1,
    markup_profile,
    markup_add_homework,
    markup_check_homework,
    markup_done,
    get_markup_dates,
    get_subjects_markup,
    markup_are_u_sure,
    markup_get_homework,
)
from BOT.tgbot.services.restapi.restapi import (
    get_subjects_by_time,
    is_admin,
    add_homework,
    get_schedule_on_date,
    delete_user,
)


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetHomework, text="fast_get"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetHomework, text="on_date_get"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["date"] = None
    await callback.message.answer(
        "Выберете день, на который хотите получить домашнее задание",
        reply_markup=get_markup_dates(await generate_dates(callback.from_user.id)),
    )


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetDate, text_contains="add_date"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    async with FSMContext.proxy() as FSMdata:
        FSMdata["date"] = date
    await callback.answer()
