from aiogram.types import Message, CallbackQuery
import datetime

from bot import dp, bot
from tgbot.handlers.shortcuts import send_homework_group
from tgbot.filters.group_filter import (
    GroupFilter,
    IsRegisteredGroupFilter,
    RegistrationGroupFilter,
)
from tgbot.services.restapi.restapi import (
    is_student,
    register_chat,
    get_homework,
    is_lessons_in_saturday,
)
from tgbot.services.scripts import generate_dates
from tgbot.services.sub_classes import RestErorr
from tgbot.keyboards.inline.markup import (
    makrup_group_menu,
    get_markup_dates,
    markup_get_homework,
)
from tgbot.FSM.states import Group
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state="*", text="menu"
)
@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state="*", text="error_menu"
)
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
        process_text(TextKeys.choose_action, msg), reply_markup=makrup_group_menu
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
            return
        await msg.answer(process_text(TextKeys.chat_registered, msg))
    else:
        await msg.answer(process_text(TextKeys.chat_unregistered, msg))


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state=Group.Menu, text="get_homework"
)
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


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state=Group.GetHomework, text="fast_get"
)
async def query_fast_get(callback: CallbackQuery):
    await callback.answer()
    date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    await send_homework_group(callback, date)


@dp.callback_query_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
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
    IsRegisteredGroupFilter(),
    state=Group.GetDate,
    text_contains="add_date",
)
async def query_return_homework(callback: CallbackQuery):
    await callback.answer()
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    await send_homework_group(callback, date)
