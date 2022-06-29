from aiogram.dispatcher.filters import BoundFilter
from aiogram import types

from tgbot.services.restapi.restapi import is_student


class GroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        return msg.chat["type"] == "group"


class IsRegisteredGroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        tguser_id = msg.from_user.id
        await is_student(tguser_id)


class RegistrationGroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        tguser_id = msg.from_user.id
        not await is_student(tguser_id)