from aiogram.types import Message, CallbackQuery

from bot import dp
from tgbot.filters.group_filter import (
    GroupFilter,
    IsRegisteredGroupFilter,
    RegistrationGroupFilter,
)
from tgbot.services.restapi.restapi import is_student, register_chat
from tgbot.services.sub_classes import RestErorr
from tgbot.keyboards.inline.markup import makrup_group_menu


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state="*", text="menu"
)
async def group_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await callback.message.answer("Выберите действие:", reply_markup=makrup_group_menu)


@dp.message_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
    state="*",
    commands=["menu", "get_hw", "get_homework"],
)
async def menu(msg: Message):
    await msg.answer("Выберите действие:", reply_markup=makrup_group_menu)


@dp.message_handler(
    GroupFilter(), RegistrationGroupFilter(), state="*", commands=["start", "register"]
)
async def registration(msg: Message):
    if await is_student(msg.from_user.id):
        res = await register_chat(msg.from_user.id, msg.chat["id"])
        if isinstance(res, RestErorr):
            return
        await msg.answer("Чат зарегистрирован. /menu - для перехода в меню")
    else:
        await msg.answer(
            "Чтобы зарегистрировать чат, нужно быть зарегистрированным пользователем в @hw_assistant_bot"
        )
