from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot import dp
from tgbot.Filters.RegistrationFilter import RegistrationFilter
from tgbot.Keyboards.Inline.Markup import Start_markup, YesOrNo_markup
from tgbot.FSM.States import RegistrationStates
from tgbot.Services.Restapi import register_user
from tgbot.Services.Scripts import time_is_correct


# Tasks:
# 1) Регистрация
# 2) Присоединение
# 3) Обработка фаст ссылок (deeplinking)


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.StartBtn, text="make_class"
)
async def NewClass_handler(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.CheckStartTime.set()
    await callback.message.answer(
        "Ваши уроки начинаются в 9:00?", reply_markup=YesOrNo_markup
    )


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckStartTime, text="check_true"
)
async def CheckStartTime_handler(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:  # запись в FSMContext ответа
        FSMdata["starttime"] = [9, 0]
    await RegistrationStates.CheckSubjects.set()
    await callback.message.answer("*Список предметов*")  # Надо проработать сообщение


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckStartTime, text="check_false"
)
async def CheckStartTime_handler(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.AddTime.set()
    await callback.message.answer(
        'Введите время начала уроков в формате: "часы:минуты"\nНапример 8:30'
    )


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.StartBtn, text="join_class_by_id"
)
async def JoinClass_handler(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.GetGroupId.set()
    await callback.message.answer(
        "Введите id класса. Его можно получить у участника класса."
    )


@dp.message_handler(RegistrationFilter(), commands=["start"], state="*")
async def Start(msg: Message):
    # !Обработка deeplinking
    FSMContext = dp.current_state(user=msg.from_user.id)
    FSMContext.reset_state()
    await msg.answer("Привет, я бот для сохранения домашки", reply_markup=Start_markup)
    await RegistrationStates.StartBtn.set()


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.AddTime)
async def AddTime_handler(msg: Message):
    time = msg.text
    FSMContext = dp.current_state(user=msg.from_user.id)
    if time_mod := time_is_correct(time):
        await msg.answer(
            f'Записано время начала уроков: "{" : ".join(time_mod)}"'
        )  # Для тестов
        async with FSMContext.proxy() as FSMdata:  # запись в FSMContext ответа
            FSMdata["starttime"] = time_mod
        await RegistrationStates.CheckSubjects.set()
        await msg.answer("*Список предметов*")
    else:
        await msg.answer("Время введено некорректно, попробуйте ещё раз")


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.GetGroupId)
async def GetId_handler(msg: Message):
    classid = msg.text
    userid = msg.from_user.id
    FSMContext = dp.current_state(user=userid)
    if register_user(userid, classid):
        await msg.answer(
            "Регистрация успешна"
        )  # Тут надо сделать отправку менюшки студента
        await FSMContext.reset_state()
    else:
        await msg.answer("Неправильный формат id")
