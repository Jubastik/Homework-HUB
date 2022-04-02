import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from tgbot.config import load_config
import tgbot.Filters
import tgbot.Handlers

logger = logging.getLogger(__name__)

# Tasks:
# 1) Реализация клавиатуры
# 2) Реализация машины состояний
# ?3) Создание Redis

async def main():
    # Логгирование
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )
    logger.info("Starting bot")
    config = load_config("bot.ini")

    # Подготовка бота
    bot = Bot(token=config.tg_bot.token)
    dp = Dispatcher(bot, storage=MemoryStorage())

    tgbot.Filters.setup(dp)  # Подключение фильтров
    tgbot.Handlers.setup(dp)  # Подключение хендлеров

    # Запуск бота
    # !Падает с ошибкой при ctrl+c: ИСПРАВИТЬ
    try:
        await dp.start_polling()
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Bot stopped!")
