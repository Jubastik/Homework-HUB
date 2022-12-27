from aiogram.types import CallbackQuery, Message
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.FSM.states import StudentClass
from tgbot.handlers.shortcuts import send_panel
from tgbot.services.scripts import time_is_correct
from tgbot.keyboards.inline.markup import (
    get_markup_classmates,
    markup_back,
    markup_mailing_disabled,
    markup_mailing_enabled,
)
from tgbot.services.restapi.restapi import (
    assign_admin,
    ban_user,
    unban_user,
    change_class_token,
    get_ban_list,
    get_names_classmates,
    get_student_info,
    class_have_chats,
    get_class,
    change_class_mailing,
    change_class_mailing_time,
)
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
        await send_panel(
            callback, status=process_text(TextKeys.no_classmates, callback)
        )
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
        await send_panel(
            callback, status=process_text(TextKeys.no_classmates, callback)
        )
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
    res = await ban_user(data[1], data[2])
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
            await send_panel(
                callback, status=process_text(TextKeys.empty_ban_list, callback)
            )
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

@dp.callback_query_handler(state=StudentClass.UnbanClassmate, text_contains="student_name")
async def query_unban_user(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")
    res = await unban_user(data[1])
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(callback, status=process_text(TextKeys.user_unbanned, callback, name=data[0]))


@dp.callback_query_handler(state=StudentClass.ClassPanel, text="mailing")
async def query_mailing(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.Mailing.set()
    res = await class_have_chats(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        if not res:
            await bot.edit_message_text(
                process_text(TextKeys.no_chats, callback),
                reply_markup=markup_back,
                chat_id=chat_id,
                message_id=main_msg_id,
            )
            return
        else:
            res = await get_class(callback.from_user.id)
            if isinstance(res, RestErorr):
                FSMContext = dp.current_state(user=callback.from_user.id)
                await FSMContext.reset_state()
                return
            if not res["mailing_stopped"]:
                await bot.edit_message_text(
                    process_text(
                        TextKeys.mailings_enabled, callback, time=res["mailing_time"]
                    ),
                    reply_markup=markup_mailing_enabled,
                    chat_id=chat_id,
                    message_id=main_msg_id,
                )
            else:
                await bot.edit_message_text(
                    process_text(
                        TextKeys.mailings_disabled, callback, time=res["mailing_time"]
                    ),
                    reply_markup=markup_mailing_disabled,
                    chat_id=chat_id,
                    message_id=main_msg_id,
                )


@dp.callback_query_handler(state=StudentClass.Mailing, text="enable_mailing")
async def query_mailing_enable(callback: CallbackQuery):
    await callback.answer()
    res = await change_class_mailing(callback.from_user.id, False)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(
        callback, status=process_text(TextKeys.status_mailings_enabled, callback)
    )


@dp.callback_query_handler(state=StudentClass.Mailing, text="disable_mailing")
async def query_mailing_disable(callback: CallbackQuery):
    await callback.answer()
    res = await change_class_mailing(callback.from_user.id, True)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(
        callback, status=process_text(TextKeys.status_mailings_disabled, callback)
    )


@dp.callback_query_handler(state=StudentClass.Mailing, text="change_time")
async def query_mailing_change_time(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.MailingTime.set()
    async with dp.current_state(user=callback.from_user.id).proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.enter_time, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_back,
        )


@dp.message_handler(state=StudentClass.MailingTime)
async def mailing_time(message: Message):
    await message.delete()
    if time_is_correct(message.text):
        res = await change_class_mailing_time(message.from_user.id, message.text)
        FSMContext = dp.current_state(user=message.from_user.id)
        if isinstance(res, RestErorr):
            await FSMContext.reset_state()
            return
        await send_panel(
            message,
            status=process_text(
                TextKeys.status_time_changed, message, time=message.text
            ),
        )
    else:
        await send_panel(
            message, status=process_text(TextKeys.status_time_incorrect, message)
        )
