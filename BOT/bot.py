from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging

from handlers import Handlers


class TgBot:
    def __init__(self, TOKEN):
        self.bot = Bot(token=TOKEN)
        self.dp = Dispatcher(self.bot, storage=MemoryStorage())  # MemoryStorage хранит инфу в оперативке
        logging.basicConfig(level=logging.INFO)
        self.hd = Handlers(self.bot, self.dp)
        self.hd.register_handlers()

    def start(self):
        executor.start_polling(self.dp, on_shutdown=self.shutdown)

    async def shutdown(self, dp: Dispatcher):
        await dp.storage.close()
        await dp.storage.wait_closed()


# Tasks:
# 1) Реализация машины состояний
# 2) Понять что такое мидлвари
# 3) Фильтры

# Следующая волна тасков
# 1) Реализация регистрации (без подключения к api)
