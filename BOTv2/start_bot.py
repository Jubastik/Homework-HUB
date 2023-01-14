import datetime
import logging
import os

from aiogram.utils import executor
from dotenv import load_dotenv

# preload
load_dotenv()

from bot import bot, dp, session

import tgbot
import tgbot.handlers
from services.everyday_mailing import activate_hw_mailing


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    from pprint import pprint
    from services.restapi.restapi import (
        get_user,
        is_student,
        is_admin,
        create_user,
        change_class_token,
        get_class,
        get_schedule,
        get_study_week_days,
        get_current_lessons,
        get_next_lesson_date,
        create_homework,
        get_homework,
        create_parser,
        get_parsed_hw,
        get_parser_status,
        delete_parser,
        get_banned_users,
        appoint_administrator,
    )
    from services.restapi.formatters import create_time_tables
    from datetime import time
    data = await appoint_administrator(3)
    print(data)

    if os.getenv("VERSION") == "server":
        # Отправка сообщения админу о запуске
        chat_id = os.getenv("TG_ADMIN_CHAT")
        bot_info = await bot.get_me()
        bot_name = bot_info["username"]
        await bot.send_message(chat_id, f"Start polling. [@{bot_name}]")
    await activate_hw_mailing()


async def on_shutdown(dp):
    if os.getenv("VERSION") == "server":
        chat_id = os.getenv("TG_ADMIN_CHAT")
        bot_info = await bot.get_me()
        bot_name = bot_info["username"]
        await bot.send_message(chat_id, f"Stop polling. [@{bot_name}]")
    await session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)


if __name__ == "__main__":
    start()
