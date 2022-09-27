from aiogram.types import CallbackQuery

from bot import dp, bot
from tgbot.handlers.shortcuts import send_panel
from tgbot.FSM.states import StudentClass
from tgbot.filters.student_filter import StudentFilter
from tgbot.filters.admin_filter import AdminFilter
from tgbot.keyboards.inline.markup import get_markup_classmates
from tgbot.services.restapi.restapi import (
    get_names_classmates,
    ban_user,
    assign_admin,
    change_class_token,
    get_student_info,
)
from tgbot.services.sub_classes import RestErorr
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="add_admin")
async def query_get_classmate(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.AddAdmin.set()
    res = await get_names_classmates(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_classmate, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_classmates(res),
        )


@dp.callback_query_handler(
    state=StudentClass.AddAdmin,
    text_contains="student_name",
)
async def query_add_admin(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")[1]
    res = await assign_admin(data)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(callback, status=process_text(TextKeys.admin_added, callback))


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="ban")
async def query_ban(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.BanClassmate.set()
    res = await get_names_classmates(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_classmate, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_classmates(res),
        )


@dp.callback_query_handler(
    state=StudentClass.BanClassmate,
    text_contains="student_name",
)
async def query_ban_user(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")[1]
    res = await ban_user(data)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(callback, status=process_text(TextKeys.user_kicked, callback))


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="remove_token")
async def query_remove_token(callback: CallbackQuery):
    await callback.answer()
    res = await change_class_token(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    res = await get_student_info(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    token = res["class_token"]
    await send_panel(
        callback, status=process_text(TextKeys.token_changed, callback, token=token)
    )
