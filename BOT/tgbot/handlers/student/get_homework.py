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
from BOT.tgbot.services.scripts import generate_dates, get_homework_on_date
from BOT.tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
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
    res = await generate_dates(callback.from_user.id)
    if isinstance(res, dict):
        await FSMContext.reset_state()
        return
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
    res = get_homework_on_date(callback.from_user.id, date)
    if not isinstance(res, dict):
        await callback.message.answer(res)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(True),
    )