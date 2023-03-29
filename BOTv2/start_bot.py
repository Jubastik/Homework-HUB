import datetime
import aiohttp
import logging
import os
import cloudpickle
import sentry_sdk

from aiogram.utils import executor
from dotenv import load_dotenv

# preload
from sentry_sdk.integrations.aiohttp import AioHttpIntegration

load_dotenv()
sentry_sdk.init(
    dsn=os.getenv("SENTRY_DSN"),
    integrations=[
        AioHttpIntegration(),
    ],
    traces_sample_rate=1.0,
    _experiments={
        "custom_measurements": True,
    },
)

from bot import bot, dp

import tgbot
import tgbot.handlers
from services.everyday_mailing import activate_hw_mailing


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    if os.getenv("USE_WEBHOOK", "False") == "True":
        logging.info("Set webhook")
        webhook_url = os.getenv("WEBHOOK_HOST") + os.getenv("WEBHOOK_PATH")
        await bot.set_webhook(webhook_url)

    headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}
    session = aiohttp.ClientSession(headers=headers)
    dp.api_session = session

    if os.getenv("VERSION") == "server":
        # Отправка сообщения админу о запуске
        chat_id = os.getenv("TG_ADMIN_CHAT")
        bot_info = await bot.get_me()
        bot_name = bot_info["username"]
        await bot.send_message(chat_id, f"Start polling. [@{bot_name}]")
    await activate_hw_mailing()


async def on_shutdown(dp):
    if os.getenv("USE_WEBHOOK", "False") == "True":
        logging.info("Delete webhook")
        await bot.delete_webhook()

    if os.getenv("VERSION") == "server":
        chat_id = os.getenv("TG_ADMIN_CHAT")
        bot_info = await bot.get_me()
        bot_name = bot_info["username"]
        await bot.send_message(chat_id, f"Stop polling. [@{bot_name}]")

    # DEPRECATED code start
    for user in bot.um.users.values():
        if user.mode and "spb_diary_get_password" in user.mode.STAGES:
            if "entry_stage" in user.mode.stages:
                user.mode.stages["entry_stage"].update_func.cancel()
                user.mode.stages["entry_stage"].update_func = None
            for task in user.mode.tasks:
                task.cancel()
            user.mode.tasks = []
    with open("um.pcl", "wb") as f:
        cloudpickle.dump(bot.um, f)
    # DEPRECATED code end

    await dp.api_session.close()
    await dp.storage.close()
    await dp.storage.wait_closed()


def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    if os.getenv("USE_WEBHOOK", "False") == "True":
        logging.info("Start webhook")
        executor.start_webhook(
            dp,
            webhook_path=os.getenv("WEBHOOK_PATH"),
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=os.getenv("WEBAPP_HOST"),
            port=int(os.getenv("WEBAPP_PORT")),
        )
    else:
        logging.info("Start polling")
        executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup, skip_updates=True)


if __name__ == "__main__":
    start()
