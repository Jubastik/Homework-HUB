from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from tgbot.services.restapi.restapi import is_unregistered


class RegistrationFilter(BoundFilter):
    async def check(self, msg: types.Message or types.CallbackQuery):
        tguser_id = msg.from_user.id
        if isinstance(msg, types.CallbackQuery):
            msg = msg.message
        return msg.chat["type"] == "private" and await is_unregistered(tguser_id)
