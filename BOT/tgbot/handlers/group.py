from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.filters.group_filter import GroupFilter, IsRegisteredGroupFilter, RegistrationGroupFilter
from tgbot.services.restapi.restapi import is_student, register_chat
from tgbot.services.sub_classes import RestErorr
from tgbot.keyboards.inline.markup import makrup_group_menu

# @dp.message_handler(GroupFilter(), state="*")
# async def dev_panel(msg: Message):
#     await msg.answer("channel /start answer")
#     await msg.answer(f"INFO ABOUT CHAT: {msg.chat}")

@dp.message_handler(GroupFilter(), IsRegisteredGroupFilter(), state="*", commands=["menu", "get_hw", "get_homework"])
async def menu(msg: Message):
    await msg.answer("Выберите действие:", reply_markup=makrup_group_menu)


@dp.message_handler(GroupFilter(), RegistrationGroupFilter(), state="*", commands=["start", "register"])
async def registration(msg: Message):
    if await is_student(msg.from_user.id):
        res = await register_chat(msg.from_user.id, msg.chat["id"])
        if isinstance(res, RestErorr):
            return
        await msg.answer("Чат зарегистрирован. /menu - для перехода в меню")
    else:
        await msg.answer("Чтобы зарегистрировать чат, нужно быть зарегистрированным пользователем в @hw_assistant_bot")