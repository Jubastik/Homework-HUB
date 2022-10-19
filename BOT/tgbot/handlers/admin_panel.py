from aiogram.types import CallbackQuery
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.filters.admin_filter import AdminFilter
from tgbot.filters.student_filter import StudentFilter
from tgbot.FSM.states import StudentClass
from tgbot.handlers.shortcuts import send_panel
from tgbot.keyboards.inline.markup import get_markup_classmates
from tgbot.services.restapi.restapi import (assign_admin, ban_user,
                                            change_class_token, get_ban_list,
                                            get_names_classmates,
                                            get_student_info)
from tgbot.services.sub_classes import RestErorr

from bot import bot, dp


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="add_admin")
async def query_get_classmate(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.AddAdmin.set()
    res = await get_names_classmates(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    if len(res) == 0:
        await send_panel(callback, status=process_text(TextKeys.no_classmates, callback))
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
    if len(res) == 0:
        await send_panel(callback, status=process_text(TextKeys.no_classmates, callback))
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
    data = callback.data.split(":")
    res = await ban_user(data[1], data[0])
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


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="unban")
async def query_unban(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.UnbanClassmate.set()
    FSMContext = dp.current_state(user=callback.from_user.id)
    ban_list = await get_ban_list(callback.from_user.id)
    if isinstance(ban_list, RestErorr):
        if ban_list.status_code == 404:
            await send_panel(callback, status=process_text(TextKeys.empty_ban_list, callback))
            return
        else:
            await FSMContext.reset_state()
            return
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_classmate, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_classmates(ban_list),
        )