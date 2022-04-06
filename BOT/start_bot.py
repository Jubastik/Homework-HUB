from aiogram import executor
import logging


from bot import dp
import tgbot.Filters, tgbot.Handlers

# Tasks:
# 1) Создание Redis
# 2) Нормальное скрытие меню а не эта фигня (ну или всё решит FSM)


async def on_startup(dp):
    # Действия при запуске, например оповещение админов
    pass


async def on_shutdown(dp):
    await dp.storage.close()
    await dp.storage.wait_closed()


def start():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    start()
