from aiogram.dispatcher.filters import BoundFilter
from aiogram import types


class GroupFilter(BoundFilter):
    async def check(self, msg: types.Message):
        return msg.chat["type"] == "group"