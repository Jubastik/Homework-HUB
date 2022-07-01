from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from tgbot.services.restapi.restapi import is_registreted_chat


class GroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        return msg.chat["type"] == "group"


class IsRegisteredGroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        chat = msg.chat.id
        return await is_registreted_chat(chat)


class RegistrationGroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        chat = msg.chat.id
        return not await is_registreted_chat(chat)