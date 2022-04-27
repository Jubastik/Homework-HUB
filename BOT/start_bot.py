import logging

from aiogram.utils import executor

import tgbot
import tgbot.filters, tgbot.handlers
from bot import dp

# Tasks:
# 1) Создание Redis
# 2) Кеширование


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    tgbot.filters.setup(dp)


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    executor.start_polling(dp)


if __name__ == "__main__":
    start()
