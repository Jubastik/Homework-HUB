from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.Filters.RegistrationFilter import RegistrationFilter
from tgbot.Keyboards.Inline.Markup import start_on, empty_markup
from tgbot.FSM.States import RegistrationStates
from tgbot.Services.Restapi import register_user


# Tasks:
# 1) Регистрация
# 2) Присоединение
# 3) Обработка фаст ссылок (deeplinking)


@dp.callback_query_handler(RegistrationFilter(), text="make_class")
async def new_class(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Создание класса")
    await callback.message.edit_reply_markup(empty_markup)


@dp.callback_query_handler(RegistrationFilter(), text="join_class_by_id")
async def join_class(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.GetGroupId.set()
    await callback.message.answer(
        "Введите id класса. Его можно получить у участника класса."
    )
    await callback.message.edit_reply_markup(empty_markup)


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.GetGroupId)
async def get_id(msg: Message):
    classid = msg.text
    userid = msg.from_user.id
    FSMContext = dp.current_state(user=userid)
    if register_user(userid, classid):
        await msg.answer(
            "Регистрация успешна"
        )  # Тут надо сделать отправку менюшки студента
        await FSMContext.finish()
    else:
        await msg.answer("Неправильный формат id")


@dp.message_handler(RegistrationFilter(), commands=["start"], state="*")
async def start(msg: Message):
    # !Обработка deeplinking
    await msg.answer("Привет, я бот для сохранения домашки.", reply_markup=start_on)
