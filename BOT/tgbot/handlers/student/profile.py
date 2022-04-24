from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
import datetime

from BOT.bot import dp
from BOT.tgbot.handlers.student.menu import query_profile
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
    StudentFilter(), state=StudentProfile.Profile, text="delete_account"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await StudentProfile.DeleteAccount.set()
    await callback.message.answer(
        "Вы уверены что хотите удалить аккаунт?", reply_markup=markup_are_u_sure
    )


# | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount |


@dp.callback_query_handler(
    StudentFilter(), state=StudentProfile.DeleteAccount, text="true"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    if await delete_user(callback.from_user.id):
        await callback.message.answer("Ваш аккаунт удалён")
        await FSMContext.reset_state()
    else:
        await callback.message.answer("Ошибка")
    # Соединение с регистрацией...


@dp.callback_query_handler(
    StudentFilter(), state=StudentProfile.DeleteAccount, text="false"
)
async def query_get_homework(callback: CallbackQuery):
    await query_profile(callback)
