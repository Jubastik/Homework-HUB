from aiogram.types import Message, CallbackQuery, InputMediaPhoto
import datetime

from bot import dp
from tgbot.filters.group_filter import (
    GroupFilter,
    IsRegisteredGroupFilter,
    RegistrationGroupFilter,
)
from tgbot.services.restapi.restapi import (
    is_student,
    register_chat,
    get_homework,
    is_lessons_in_saturday,
)
from tgbot.services.scripts import convert_homework, generate_dates
from tgbot.services.sub_classes import RestErorr
from tgbot.keyboards.inline.markup import (
    makrup_group_menu,
    get_markup_student_menu,
    get_markup_dates,
    markup_get_homework
)
from tgbot.FSM.states import Group


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state="*", text="menu"
)
async def group_menu(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await callback.message.answer("Выберите действие:", reply_markup=makrup_group_menu)


@dp.message_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
    state="*",
    commands=["menu", "get_hw", "get_homework"],
)
async def menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await Group.Menu.set()
    await msg.answer("Выберите действие:", reply_markup=makrup_group_menu)


@dp.message_handler(
    GroupFilter(),
    RegistrationGroupFilter(),
    state="*",
    commands=["start", "register", "menu"],
)
async def registration(msg: Message):
    if await is_student(msg.from_user.id):
        res = await register_chat(msg.from_user.id, msg.chat["id"])
        if isinstance(res, RestErorr):
            return
        await msg.answer("Чат зарегистрирован. /menu - для перехода в меню")
    else:
        await msg.answer(
            "Чтобы зарегистрировать чат, нужно быть зарегистрированным пользователем в @hw_assistant_bot"
        )


@dp.callback_query_handler(GroupFilter(), IsRegisteredGroupFilter(), state=Group.Menu, text="get_homework")
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await Group.GetHomework.set()
    await callback.message.answer(
        "Меню выбора получения домашки", reply_markup=markup_get_homework
    )


async def send_homework(callback: CallbackQuery, date):
    res = await get_homework(callback.message.chat.id, date, is_chat=True)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    data = await convert_homework(res[0])
    for lesson in data:
        if len(lesson["photos"]) != 0:
            media = [InputMediaPhoto(lesson["photos"][0], lesson["text"])]
            for photo in lesson["photos"][1:]:
                media.append(InputMediaPhoto(photo))
            await callback.message.answer_media_group(
                media,
                disable_notification=True,
            )
        else:
            await callback.message.answer(lesson["text"])
    await FSMContext.reset_state()
    await Group.Menu.set()


@dp.callback_query_handler(
    GroupFilter(), IsRegisteredGroupFilter(), state=Group.GetHomework, text="fast_get"
)
async def query_fast_get(callback: CallbackQuery):
    await callback.answer()
    date = datetime.datetime.now().date() + datetime.timedelta(days=1)
    await send_homework(callback, date)


@dp.callback_query_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
    state=Group.GetHomework,
    text="on_date_get",
)
async def query_get_date(callback: CallbackQuery):
    await callback.answer()
    res = await is_lessons_in_saturday(callback.from_user.id)
    FSMContext = dp.current_state(user=callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await Group.GetDate.set()
    await callback.message.answer(
        "Выберете день, на который хотите получить домашнее задание",
        reply_markup=get_markup_dates(generate_dates(res)),
    )


@dp.callback_query_handler(
    GroupFilter(),
    IsRegisteredGroupFilter(),
    state=Group.GetDate,
    text_contains="add_date",
)
async def query_return_homework(callback: CallbackQuery):
    await callback.answer()
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    await send_homework(callback, date)
