from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
import datetime

from BOT.bot import dp
from BOT.tgbot.FSM.states import StudentAddHomework, StudentProfile, StudentMenu, StudentGetHomework, StudentClass
from BOT.tgbot.filters.student_filter import StudentFilter
from BOT.tgbot.filters.admin_filter import AdminFilter
from BOT.tgbot.services.scripts import generate_dates
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


@dp.message_handler(AdminFilter(), commands=["admin_panel"], state="*")
async def admin_panel(msg: Message):
    await msg.answer("Админка")


# 1) [{tg_id: student_name}]
# 2) {name: str, is_admin: Bool, class_token: int, admins: [str, str]}
# 3) str