from json.encoder import INFINITY
from aiogram.types import Message, CallbackQuery

from bot import dp
from tgbot.Filters.RegistrationFilter import RegistrationFilter
from tgbot.Keyboards.Inline.markup import start_on, empty

# Tasks:
# 1) Регистрация
# 2) Присоединение
# 3) Обработка фаст ссылок (deeplinking)


@dp.message_handler(RegistrationFilter(), commands=["start"], state="*")
async def start(msg: Message):
    await msg.answer("Привет, я бот для сохранения домашки.", reply_markup=start_on)


@dp.callback_query_handler(RegistrationFilter(), text="make_class")
async def new_class(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Создание класса")
    await callback.message.edit_reply_markup(empty)


@dp.callback_query_handler(RegistrationFilter(), text="join_class_by_id")
async def join_class(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "Введите id класса. Его можно получить у участника класса."
    )
    await callback.message.edit_reply_markup(empty)
