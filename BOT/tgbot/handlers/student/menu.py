from aiogram.types import Message, CallbackQuery

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
from BOT.tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    markup_profile,
    markup_add_homework,
    markup_get_homework,
)
from BOT.tgbot.services.restapi.restapi import is_admin, get_student_info
from BOT.tgbot.services.sub_classes import RestErorr
from BOT.tgbot.services.scripts import convert_user_info


@dp.callback_query_handler(StudentFilter(), state=StudentMenu.Menu, text="profile")
async def query_profile(callback: CallbackQuery):
    await callback.answer()
    res = await get_student_info(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    txt = convert_user_info(res)
    await StudentProfile.Profile.set()
    await callback.message.answer(
        txt, reply_markup=markup_profile
    )


@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentMenu.Menu, text="class_menu"
)
async def query_class_menu(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.ClassPanel.set()
    await callback.message.answer("Панель управления классом")


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
async def hanldler_menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    await msg.answer(
        "Меню", reply_markup=get_markup_student_menu(await is_admin(msg.from_user.id))
    )


@dp.callback_query_handler(StudentFilter(), state="*", text="menu")
async def query_menu(callback: CallbackQuery):
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(await is_admin(callback.from_user.id)),
    )
