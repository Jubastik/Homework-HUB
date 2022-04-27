from aiogram.types import Message, CallbackQuery

from bot import dp
from tgbot.FSM.states import (
    StudentAddHomework,
    StudentProfile,
    StudentMenu,
    StudentGetHomework,
    StudentClass,
)
from tgbot.filters.student_filter import StudentFilter
from tgbot.filters.admin_filter import AdminFilter
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    markup_profile,
    markup_add_homework,
    markup_get_homework,
    markup_class_panel,
)
from tgbot.services.restapi.restapi import is_admin, get_student_info, get_names_classmates
from tgbot.services.sub_classes import RestErorr
from tgbot.services.scripts import convert_user_info, convert_users


@dp.callback_query_handler(StudentFilter(), state=StudentMenu.Menu, text="profile")
async def query_profile(callback: CallbackQuery):
    await callback.answer()
    res = await get_student_info(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    txt = convert_user_info(res)
    await StudentProfile.Profile.set()
    await callback.message.answer(txt, reply_markup=markup_profile)


@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentMenu.Menu, text="class_menu"
)
async def query_class_menu(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.ClassPanel.set()
    res = await get_names_classmates(callback.from_user.id)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        FSMContext.reset_state()
        return
    txt = convert_users(res)
    await callback.message.answer(
        txt, reply_markup=markup_class_panel
    )


@dp.callback_query_handler(StudentFilter(), state=StudentMenu.Menu, text="add_homework")
async def query_add_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        # Установка дефолтных значений
        FSMdata["subject"] = None
        FSMdata["is_fast"] = None
        FSMdata["date"] = None
        FSMdata["text"] = ""
        FSMdata["files_tgid"] = []
        FSMdata["msg_id"] = False
    await StudentAddHomework.AddHomework.set()
    await callback.message.answer(
        "Выбери способ добавления", reply_markup=markup_add_homework
    )


@dp.callback_query_handler(StudentFilter(), state=StudentMenu.Menu, text="get_homework")
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await StudentGetHomework.GetHomework.set()
    await callback.message.answer(
        "Меню выбора получения домашки", reply_markup=markup_get_homework
    )


@dp.message_handler(StudentFilter(), commands=["start", "menu"], state="*")
async def handler_menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(msg.from_user.id)
    if isinstance(res, RestErorr):
        return
    await msg.answer(
        "Меню", reply_markup=get_markup_student_menu(res)
    )


@dp.callback_query_handler(StudentFilter(), state="*", text="menu")
async def query_menu(callback: CallbackQuery):
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(res),
    )
