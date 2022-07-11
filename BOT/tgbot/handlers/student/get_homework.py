from aiogram.types import CallbackQuery
import datetime

from bot import dp, bot
from tgbot.handlers.shortcuts import send_homework
from tgbot.FSM.states import StudentGetHomework
from tgbot.filters.student_filter import StudentFilter
from tgbot.services.scripts import generate_dates
from tgbot.keyboards.inline.markup import get_markup_dates
from tgbot.services.restapi.restapi import is_lessons_in_saturday
from tgbot.services.sub_classes import RestErorr
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


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
    async with FSMContext.proxy() as FSMdata:
        await StudentGetHomework.GetDate.set()
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_date, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
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
