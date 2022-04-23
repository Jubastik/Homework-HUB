from aiogram.types import Message, CallbackQuery, ContentType
from aiogram.dispatcher import FSMContext
import datetime

from BOT.bot import dp
from BOT.tgbot.FSM.states import StudentStates
from BOT.tgbot.filters.student_filter import StudentFilter
from BOT.tgbot.filters.admin_filter import AdminFilter
from BOT.tgbot.services.scripts import generate_dates
from BOT.tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    get_markup_fast_add1,
    markup_profile,
    markup_add_homework,
    markup_check_homework,
    markup_done,
    get_markup_dates,
    get_subjects_markup,
    markup_are_u_sure,
    markup_get_homework,
)
from BOT.tgbot.services.restapi.restapi import (
    get_subjects_by_time,
    is_admin,
    add_homework,
    get_schedule_on_date,
    delete_user,
)


# | Student Menu | Student Menu | Student Menu | Student Menu | Student Menu | Student Menu | Student Menu | Student Menu |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.StudentMenu, text="profile"
)
async def query_profile(callback: CallbackQuery):
    await callback.answer()
    await StudentStates.Profile.set()
    await callback.message.answer(
        "Профиль: ...\nINFO ABOUT USER", reply_markup=markup_profile
    )  # In work


@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentStates.StudentMenu, text="class_menu"
)
async def query_class_menu(callback: CallbackQuery):
    await callback.answer()
    await StudentStates.ClassPanel.set()
    await callback.message.answer("Панель управления классом")


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.StudentMenu, text="add_homework"
)
async def query_add_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        # Установка дефолтных значений
        FSMdata["subject"] = None
        FSMdata["is_fast"] = None
        FSMdata["date"] = None
        FSMdata["text"] = ""
        FSMdata["files_tgid"] = []
        FSMdata["msg_id"] = False
    await StudentStates.AddHomework.set()
    await callback.message.answer(
        "Выбери способ добавления", reply_markup=markup_add_homework
    )


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.StudentMenu, text="get_homework"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        # Установка дефолтных значений
        pass
    await StudentStates.GetHomework.set()
    await callback.message.answer(
        "Меню выбора получения домашки", reply_markup=markup_get_homework
    )


# | GetHomework | GetHomework | GetHomework | GetHomework | GetHomework | GetHomework | GetHomework | GetHomework |





# | Profile | Profile | Profile | Profile | Profile | Profile | Profile | Profile |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.Profile, text="delete_account"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await StudentStates.DeleteAccount.set()
    await callback.message.answer(
        "Вы уверены что хотите удалить аккаунт?", reply_markup=markup_are_u_sure
    )


# | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.DeleteAccount, text="true"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    if await delete_user(callback.from_user.id):
        await callback.message.answer("Ваш аккаунт удалён")
    else:
        await callback.message.answer("Ошибка")
    # Соединение с регистрацией...


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.DeleteAccount, text="false"
)
async def query_get_homework(callback: CallbackQuery):
    await query_profile(callback)  # ахахахах, оказываается так можно было...


# | Add Homework | Add Homework | Add Homework | Add Homework | Add Homework | Add Homework | Add Homework | Add Homework |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.AddHomework, text="fast_add"
)
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    # Получение 2-х предметов по текущему времени из БД
    userid = callback.from_user.id
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["is_fast"] = True
    await StudentStates.FastAdd.set()
    await callback.message.answer(
        "На какой предмет добавить дз?",
        reply_markup=get_markup_fast_add1(await get_subjects_by_time(userid)),
    )


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.AddHomework, text="on_date_add"
)
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["is_fast"] = False
    await StudentStates.GetDate.set()
    await callback.message.answer(
        "Выберете дату, на которую хотите добавить домашнее задание:",
        reply_markup=get_markup_dates(await generate_dates(callback.from_user.id)),
    )


# | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.GetDate, text_contains="add_date"
)
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    async with FSMContext.proxy() as FSMdata:
        FSMdata["date"] = date
    await StudentStates.GetSubjects.set()
    await callback.message.answer(
        f"Выберете предмет из расписания на {date}",
        reply_markup=get_subjects_markup(
            await get_schedule_on_date(callback.from_user.id, date)
        ),
    )


# | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.GetSubjects, text_contains="subject"
)
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    subject = callback.data.split(":")[1]
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["subject"] = subject
    await StudentStates.WaitHomework.set()
    await callback.message.answer(
        "Отправьте домашнее задание👇🏻 (можно прикрепить фото)", reply_markup=markup_done
    )


# | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.FastAdd, text_contains="subject"
)
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["subject"] = callback.data.split(":")[1]
    await StudentStates.WaitHomework.set()
    await callback.message.answer(
        "Отправьте домашнее задание👇🏻 (можно прикрепить фото)", reply_markup=markup_done
    )


# | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework |


@dp.message_handler(
    StudentFilter(), state=StudentStates.WaitHomework, content_types=ContentType.ANY
)
async def hanldler_wait_homework(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if msg.text or msg.caption:
            FSMdata["text"] = f"{FSMdata['text']}\n{(msg.text or msg.caption)}".lstrip()
        if msg.photo:
            FSMdata["files_tgid"].append(msg.photo[-1].file_id)


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.WaitHomework, text="done"
)
async def query_homework_check(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if FSMdata["text"] is None and len(FSMdata["files_tgid"]) == 0:
            await callback.message.answer("Не получено никакой информации")
        else:
            await StudentStates.CheckHomework.set()
            await callback.message.answer(
                "\n".join(
                    [
                        f"Записываю домашнее задание на *число* {FSMdata['subject']}",
                        "Верно?",
                    ]
                ),
                reply_markup=markup_check_homework,
            )


# | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework |


@dp.callback_query_handler(
    StudentFilter(), state=StudentStates.CheckHomework, text_contains="check_homework"
)
async def query_homework_check(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")[1]
    FSMContext = dp.current_state(user=callback.from_user.id)
    if data == "true":
        async with FSMContext.proxy() as FSMdata:
            userid = callback.from_user.id
            params = {
                "subject": FSMdata["subject"],
                "text": FSMdata["text"],
                "files_tgid": FSMdata["files_tgid"],
                "date": FSMdata["date"],
            }
            res = await add_homework(userid, params, auto=FSMdata["is_fast"])
            if res is True:
                await callback.message.answer("Домашнее задание успешно записано")

            else:
                await callback.message.answer(f"Error: {res}")
    else:
        await callback.message.answer(
            'Попробуйте добавить домашку через функцию "Добавить на дату"'
        )
    await FSMContext.reset_state()
    await StudentStates.StudentMenu.set()
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(await is_admin(callback.from_user.id)),
    )


# | General handlers | General handlers | General handlers | General handlers | General handlers | General handlers | General handlers | General handlers |
# Хендлеры, реагирующие на 2+ состояния


@dp.message_handler(StudentFilter(), commands=["start", "menu"], state="*")
async def hanldler_menu(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    await FSMContext.reset_state()
    await StudentStates.StudentMenu.set()
    await msg.answer(
        "Меню", reply_markup=get_markup_student_menu(await is_admin(msg.from_user.id))
    )


@dp.callback_query_handler(StudentFilter(), state="*", text="menu")
async def query_menu(callback: CallbackQuery):
    FSMContext = dp.current_state(user=callback.from_user.id)
    await FSMContext.reset_state()
    await StudentStates.StudentMenu.set()
    await callback.message.answer(
        "Меню",
        reply_markup=get_markup_student_menu(await is_admin(callback.from_user.id)),
    )
