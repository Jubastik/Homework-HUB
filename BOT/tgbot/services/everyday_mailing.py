import asyncio
import datetime

from aiogram.types import InputMediaPhoto
from tgbot.services.restapi.restapi import get_all_mailings, get_homework, get_study_days
from tgbot.services.sub_classes import RestErorr

from bot import bot


def get_seconds_to_event(event_time) -> int:
    now = datetime.datetime.now()
    event_time = datetime.datetime.combine(now.date(), event_time)
    if event_time < now:
        event_time += datetime.timedelta(days=1)
    return (event_time - now).seconds


class Mailing:
    def __init__(self, class_id, time, chat_id):
        self.class_id = class_id
        self.tguser_id = ...
        self.time = time
        self.chat_id = chat_id
        self.disabled = False


    async def start_mailing(self):  # Рассылка
        time = get_seconds_to_event(datetime.time(*self.time.split(":")))
        while True:
            await asyncio.sleep(time)
            if self.disabled:
                return
            date = datetime.datetime.now().date() + datetime.timedelta(days=1)
            await self.send_hw_mailing(self.id, date, is_chat=True)
            time = 86400  # 24h = 86400s


    async def send_hw_mailing(self, date, is_chat=False):  # Отправляет домашку
        data = await get_homework(self.tguser_id, date, is_chat=is_chat, except_404=True, messages=True)
        if isinstance(data, RestErorr):
            return
        for lesson in data:
            if len(lesson["photos"]) != 0:
                media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
                for photo in lesson["photos"][1:]:
                    media.append(InputMediaPhoto(photo))
                await bot.send_media_group(self.chat_id, media, disable_notification=True)
            else:
                await bot.send_message(self.chat_id, lesson["text"], disable_notification=True)


async def activate_hw_mailing():  # Запускает рассылки
    # data = await get_all_mailings()
    print("Mailing: IN DEVELOPMENT")
    # for mailing in data:
    #     pass

# TODO: Реализовать рассылку дз