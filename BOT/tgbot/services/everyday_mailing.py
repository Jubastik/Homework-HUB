import asyncio
import datetime

from aiogram.types import InputMediaPhoto
from tgbot.services.restapi.restapi import get_all_mailings, get_homework
from tgbot.services.sub_classes import RestErorr

from bot import bot


def get_seconds_to_event(event_time) -> int:
    now = datetime.datetime.now()
    event_time = datetime.datetime.combine(now.date(), event_time)
    if event_time < now:
        event_time += datetime.timedelta(days=1)
    return (event_time - now).seconds


async def make_mailing(id: int, time: str, weekdays: list):  # Рассылка
    time = get_seconds_to_event(datetime.time(*time.split(":")))
    is_chat = id < 0
    while True:
        await asyncio.sleep(time)
        date = datetime.datetime.now() + datetime.timedelta(days=1)
        if date.weekday() in weekdays:
            await send_hw_mailing(id, date, is_chat=is_chat)
        time = 86400  # 24h = 86400s


async def send_hw_mailing(id, date, is_chat=False):  # Отправляет домашку
    data = await get_homework(id, date, is_chat=is_chat)
    if isinstance(data, RestErorr):
        return
    for lesson in data:
        if len(lesson["photos"]) != 0:
            media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
            for photo in lesson["photos"][1:]:
                media.append(InputMediaPhoto(photo))
            await bot.send_media_group(id, media, disable_notification=True)
        else:
            await bot.send_message(lesson["text"], disable_notification=True)


async def activate_hw_mailing():  # Запускает рассылки
    data = await get_all_mailings()
