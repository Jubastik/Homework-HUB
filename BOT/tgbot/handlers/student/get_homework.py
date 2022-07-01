from aiogram.types import Message, CallbackQuery, ContentType, InputMediaPhoto
import datetime

from bot import dp
from tgbot.FSM.states import (
    StudentMenu,
    StudentGetHomework,
)
from tgbot.filters.student_filter import StudentFilter
from tgbot.services.scripts import generate_dates, convert_homework
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    get_markup_dates,
)
from tgbot.services.restapi.restapi import (
    get_homework,
    is_lessons_in_saturday,
)
from tgbot.services.sub_classes import RestErorr


async def send_homework(callback: CallbackQuery, date):
    res = await get_homework(callback.from_user.id, date)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    data = await convert_homework(res[0])
    for lesson in data:
        if len(lesson["photos"]) != 0:
            media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
            for photo in lesson["photos"][1:]:
                media.append(InputMediaPhoto(photo))
            await callback.message.answer_media_group(
                media,
                disable_notification=True,
            )
        else:
            await callback.message.answer(lesson["text"])
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(True),
    )


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetHomework, text="fast_get"
)
async def query_fast_get(callback: CallbackQuery):
    await callback.answer()
    date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    await send_homework(callback, date)


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetHomework, text="on_date_get"
)
async def query_get_date(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await is_lessons_in_saturday(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await StudentGetHomework.GetDate.set()
    await callback.message.answer(
        "Выберете день, на который хотите получить домашнее задание",
        reply_markup=get_markup_dates(generate_dates(res)),
    )


@dp.callback_query_handler(
    StudentFilter(), state=StudentGetHomework.GetDate, text_contains="add_date"
)
async def query_return_homework(callback: CallbackQuery):
    await callback.answer()
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    await send_homework(callback, date)
