import logging
import os

from aiogram.utils import executor
from dotenv import load_dotenv

# preload
load_dotenv()

from bot import bot, dp

import tgbot
import tgbot.handlers
from services.everyday_mailing import activate_hw_mailing


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    from services.restapi.restapi import get_student
    res = await get_student()
    print(res)
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
