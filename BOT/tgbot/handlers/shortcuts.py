from aiogram.types import CallbackQuery, InputMediaPhoto
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.FSM.states import Group, StudentClass, StudentMenu
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    markup_class_panel,
    markup_start,
)
from tgbot.services.restapi.restapi import get_homework, is_admin
from tgbot.services.scripts import convert_homework
from tgbot.services.sub_classes import RestErorr

from bot import bot, dp


async def send_panel(callback: CallbackQuery, status=""):
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentClass.ClassPanel.set()
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.class_panel, callback, status=status),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_class_panel,
        )


async def send_homework(callback: CallbackQuery, date):
    res = await get_homework(callback.from_user.id, date)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    data = await convert_homework(res[0], callback)
    for lesson in data:
        if len(lesson["photos"]) != 0:
            media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
            for photo in lesson["photos"][1:]:
                media.append(InputMediaPhoto(photo))
            await callback.message.answer_media_group(
                media,
                disable_notification=True,
            )
        else:
            await callback.message.answer(lesson["text"])
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    msg = await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(res),
    )
    async with FSMContext.proxy() as FSMdata:
        FSMdata["main_msg_id"] = msg.message_id


async def send_homework_group(callback: CallbackQuery, date):
    res = await get_homework(callback.message.chat.id, date, is_chat=True)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    data = await convert_homework(res[0])
    for lesson in data:
        if len(lesson["photos"]) != 0:
            media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
            for photo in lesson["photos"][1:]:
                media.append(InputMediaPhoto(photo))
            await callback.message.answer_media_group(
                media,
                disable_notification=True,
            )
        else:
            await callback.message.answer(lesson["text"])
    await FSMContext.reset_state()
    await Group.Menu.set()


async def back_to_registration_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        await bot.edit_message_text(
            process_text(TextKeys.hello, callback),
            chat_id=callback.from_user.id,
            message_id=main_msg_id,
            reply_markup=markup_start,
        )
