from aiogram.types import Message, CallbackQuery

from bot import dp, bot
from tgbot.handlers.shortcuts import send_panel
from CONSTANTS import TG_BOT_LINK
from tgbot.FSM.states import (
    StudentAddHomework,
    StudentProfile,
    StudentMenu,
    StudentGetHomework,
)
from tgbot.filters.student_filter import StudentFilter
from tgbot.filters.admin_filter import AdminFilter
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    markup_profile,
    markup_add_homework,
    markup_get_homework,
)
from tgbot.services.restapi.restapi import (
    is_admin,
    get_student_info,
)
from tgbot.services.sub_classes import RestErorr
from languages.text_proccesor import process_text
from languages.text_keys import TextKeys


@dp.callback_query_handler(state=StudentMenu.Menu, text="profile")
async def query_profile(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await get_student_info(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    async with FSMContext.proxy() as FSMdata:
        res["is_admin"] = "✅" if res["is_admin"] else "❌"
        res["admins"] = " ".join(["@" + i for i in res["admins"]])
        res["link"] = TG_BOT_LINK
        await StudentProfile.Profile.set()
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.profile, callback, **res),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_profile,
        )


@dp.callback_query_handler(AdminFilter(), state=StudentMenu.Menu, text="class_menu")
async def query_class_menu(callback: CallbackQuery):
    await callback.answer()
    await send_panel(callback)


@dp.callback_query_handler(state=StudentMenu.Menu, text="add_homework")
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
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_homework, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_add_homework,
        )


@dp.callback_query_handler(state=StudentMenu.Menu, text="get_homework")
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await StudentGetHomework.GetHomework.set()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.homework_menu, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_get_homework,
        )


@dp.message_handler(StudentFilter(), commands=["start", "menu"], state="*")
async def handler_menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(msg.from_user.id)
    if isinstance(res, RestErorr):
        return
    async with FSMContext.proxy() as FSMdata:
        msg = await msg.answer(
            process_text(TextKeys.menu, msg), reply_markup=get_markup_student_menu(res)
        )
        FSMdata["main_msg_id"] = msg.message_id


@dp.callback_query_handler(StudentFilter(), state="*", text="menu")
async def query_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentMenu.Menu.set()
    res = await is_admin(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.menu, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_student_menu(res),
        )


@dp.callback_query_handler(StudentFilter(), state="*", text="error_menu")
async def query_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(callback.from_user.id)
    if isinstance(res, RestErorr):
        return
    async with FSMContext.proxy() as FSMdata:
        msg = await callback.message.answer(
            process_text(TextKeys.menu, callback),
            reply_markup=get_markup_student_menu(res),
        )
        FSMdata["main_msg_id"] = msg.message_id
