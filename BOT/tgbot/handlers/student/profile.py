import datetime

from aiogram.types import CallbackQuery
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.filters.student_filter import StudentFilter
from tgbot.FSM.states import StudentProfile
from tgbot.handlers.shortcuts import send_homework
from tgbot.handlers.student.menu import query_profile
from tgbot.keyboards.inline.markup import (get_markup_dates, markup_are_u_sure,
                                           markup_back)
from tgbot.services.restapi.restapi import (delete_user, get_shedule,
                                            get_study_days)
from tgbot.services.scripts import generate_dates_back
from tgbot.services.sub_classes import RestErorr

from bot import bot, dp


@dp.callback_query_handler(state=StudentProfile.Profile, text="delete_account")
async def query_delete_watning(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentProfile.DeleteAccount.set()
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.delete_account, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_are_u_sure,
        )


# | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount |


@dp.callback_query_handler(state=StudentProfile.DeleteAccount, text="true")
async def query_delete_true(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await delete_user(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await callback.message.answer("Ваш аккаунт удалён")
    await FSMContext.reset_state()
    # Соединение с регистрацией...


@dp.callback_query_handler(state=StudentProfile.DeleteAccount, text="false")
@dp.callback_query_handler(state=StudentProfile.Shedule, text="back")
async def query_delete_false(callback: CallbackQuery):
    await query_profile(callback)


# | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule |


@dp.callback_query_handler(state=StudentProfile.Profile, text="get_shedule")
async def query_delete_true(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentProfile.Shedule.set()
    res = await get_shedule(callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        msgid = FSMdata["main_msg_id"]
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await bot.edit_message_text(
        process_text(
            TextKeys.shedule3,
            callback,
            **res.get_formatted_shedule(),
        ),
        chat_id=callback.message.chat.id,
        message_id=msgid,
        reply_markup=markup_back,
    )


# | homework_history | homework_history | homework_history | homework_history | homework_history | homework_history | homework_history | homework_history |


@dp.callback_query_handler(state=StudentProfile.Profile, text="get_homework_history")
async def homework_history_dates(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentProfile.HomeworkHistoryDates.set()
    days = await get_study_days(callback.from_user.id)
    dates = generate_dates_back(days)
    async with FSMContext.proxy() as FSMdata:
        msgid = FSMdata["main_msg_id"]
    print(f"days: {days}")
    await bot.edit_message_text(
        process_text(TextKeys.homework_history_dates, callback),
        chat_id=callback.message.chat.id,
        message_id=msgid,
        reply_markup=get_markup_dates(dates),
    )


@dp.callback_query_handler(
    state=StudentProfile.HomeworkHistoryDates, text_contains="date"
)
async def get_homework_history(callback: CallbackQuery):
    await callback.answer()
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    await send_homework(callback, date)
