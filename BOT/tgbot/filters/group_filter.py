from aiogram import types
from aiogram.dispatcher.filters import BoundFilter
from tgbot.services.restapi.restapi import is_registreted_chat


class GroupFilter(BoundFilter):
    async def check(self, msg: types.Message or types.CallbackQuery):
        if isinstance(msg, types.CallbackQuery):
            msg = msg.message
        return msg.chat["type"] == "group"


class IsRegisteredGroupFilter(BoundFilter):
    async def check(self, msg: types.Message or types.CallbackQuery):
        if isinstance(msg, types.CallbackQuery):
            msg = msg.message
        return await is_registreted_chat(msg.chat.id)


class RegistrationGroupFilter(BoundFilter):
    async def check(self, msg: types.Message or types.CallbackQuery):
        if isinstance(msg, types.CallbackQuery):
            msg = msg.message
        return not await is_registreted_chat(msg.chat.id)
