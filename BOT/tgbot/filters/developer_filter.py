from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from BOT.tgbot.services.restapi.restapi import is_developer


class DeveloperFilter(BoundFilter):
    async def check(self, msg: types.Message):
        tguser_id = msg.from_user.id
        return await is_developer(tguser_id)