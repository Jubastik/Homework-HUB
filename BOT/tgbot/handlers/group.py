import datetime

from aiogram.types import CallbackQuery, Message
from CONSTANTS import TG_BOT_LINK
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.filters.group_filter import (GroupFilter, IsRegisteredGroupFilter,
                                        RegistrationGroupFilter)
from tgbot.FSM.states import Group
from tgbot.handlers.shortcuts import send_homework_group
from tgbot.keyboards.inline.markup import (get_markup_dates, makrup_group_menu,
                                           markup_get_homework)
from tgbot.services.restapi.restapi import (get_student_info,
                                            is_lessons_in_saturday, is_student,
                                            register_chat)
from tgbot.services.scripts import generate_dates
from tgbot.services.sub_classes import RestErorr

from bot import bot, dp


@dp.callback_query_handler(GroupFilter(), state="*", text="menu")
@dp.callback_query_handler(GroupFilter(), state="*", text="error_menu")
async def group_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await Group.Menu.set()
    message = await callback.message.answer(
        process_text(TextKeys.choose_action, callback),
        reply_markup=makrup_group_menu,
        disable_notification=True,
    )
    async with FSMContext.proxy() as FSMdata:
        FSMdata["main_msg_id"] = message.message_id


@dp.message_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
    state="*",
    commands=["menu", "get_hw", "get_homework", "start"],
)
async def menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await Group.Menu.set()
    message = await msg.answer(
        process_text(TextKeys.choose_action, msg),
        reply_markup=makrup_group_menu,
        disable_notification=True,
    )
    async with FSMContext.proxy() as FSMdata:
        FSMdata["main_msg_id"] = message.message_id


@dp.message_handler(
    GroupFilter(),
    RegistrationGroupFilter(),
    state="*",
    commands=["start", "register", "menu"],
)
async def registration(msg: Message):
    if await is_student(msg.from_user.id):
        res = await register_chat(msg.from_user.id, msg.chat["id"])
        if isinstance(res, RestErorr):
            FSMContext = dp.current_state(user=msg.from_user.id)
            await FSMContext.reset_state()
            return
        res = await get_student_info(msg.from_user.id)
        if isinstance(res, RestErorr):
            FSMContext = dp.current_state(user=msg.from_user.id)
            await FSMContext.reset_state()
            return
        link = TG_BOT_LINK + str(res["class_token"])
        await msg.answer(
            process_text(TextKeys.chat_registered, msg, link=link),
            disable_notification=True,
        )
    else:
        await msg.answer(
            process_text(TextKeys.chat_unregistered, msg), disable_notification=True
        )


@dp.callback_query_handler(GroupFilter(), state=Group.Menu, text="get_homework")
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await Group.GetHomework.set()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.message.chat.id
        await bot.edit_message_text(
            process_text(TextKeys.homework_menu, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_get_homework,
        )


@dp.callback_query_handler(GroupFilter(), state=Group.GetHomework, text="fast_get")
async def query_fast_get(callback: CallbackQuery):
    await callback.answer()
    date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    await send_homework_group(callback, date)


@dp.callback_query_handler(
    GroupFilter(),
    state=Group.GetHomework,
    text="on_date_get",
)
async def query_get_date(callback: CallbackQuery):
    await callback.answer()
    res = await is_lessons_in_saturday(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await Group.GetDate.set()
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.message.chat.id
        await bot.edit_message_text(
            process_text(TextKeys.date_menu, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_dates(generate_dates(res)),
        )


@dp.callback_query_handler(
    GroupFilter(),
    state=Group.GetDate,
    text_contains="add_date",
)
async def query_return_homework(callback: CallbackQuery):
    await callback.answer()
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    await send_homework_group(callback, date)
