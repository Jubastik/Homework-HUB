from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.filters.group_filter import GroupFilter, IsRegisteredGroupFilter, RegistrationGroupFilter
from tgbot.services.restapi.restapi import is_student


# @dp.message_handler(GroupFilter(), state="*")
# async def dev_panel(msg: Message):
#     await msg.answer("channel /start answer")
#     await msg.answer(f"INFO ABOUT CHAT: {msg.chat}")

@dp.message_handler(GroupFilter(), RegistrationGroupFilter(), state="*", commands=["/start", "/register"])
async def dev_panel(msg: Message):
    if is_student(msg.from_user):
        tg_id = msg.chat.id
    else:
        pass


# class_id = (
#     db_sess.query(Class.id)
#     .filter(Class.class_token == data["class_token"])
#     .first()
# )