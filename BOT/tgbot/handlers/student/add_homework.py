from aiogram.types import Message, CallbackQuery, ContentType
import datetime

from bot import dp, bot
from tgbot.FSM.states import (
    StudentAddHomework,
    StudentMenu,
)
from tgbot.filters.student_filter import StudentFilter
from tgbot.services.scripts import generate_dates
from tgbot.keyboards.inline.markup import (
    get_markup_student_menu,
    markup_check_homework,
    markup_done,
    get_markup_dates,
    get_subjects_markup,
)
from tgbot.services.restapi.restapi import (
    get_subjects_by_time,
    add_homework,
    get_schedule_on_date,
    is_lessons_in_saturday,
)
from tgbot.services.sub_classes import RestErorr
from languages.text_proccesor import process_text
from languages.text_keys import TextKeys


@dp.callback_query_handler(state=StudentAddHomework.AddHomework, text="fast_add")
async def query_fast_add(callback: CallbackQuery):
    await callback.answer()
    # Получение 2-х предметов по текущему времени из БД
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await get_subjects_by_time(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        FSMdata["is_fast"] = True
        await StudentAddHomework.FastAdd.set()
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_subject, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_subjects_markup(res),
        )


@dp.callback_query_handler(state=StudentAddHomework.AddHomework, text="on_date_add")
async def query_add_on_date(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await is_lessons_in_saturday(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        FSMdata["is_fast"] = False
        await StudentAddHomework.GetDate.set()
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_date, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=get_markup_dates(generate_dates(res)),
        )


# | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date | Add on date |


@dp.callback_query_handler(state=StudentAddHomework.GetDate, text_contains="add_date")
async def query_get_date(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    str_date = list(map(int, callback.data.split(":")[1].split("-")))
    date = datetime.date(year=str_date[0], month=str_date[1], day=str_date[2])
    res = await get_schedule_on_date(callback.from_user.id, date)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    async with FSMContext.proxy() as FSMdata:
        FSMdata["date"] = date
        await StudentAddHomework.GetSubjects.set()
        main_message_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.choose_subject_on_date, callback, date=date),
            chat_id=chat_id,
            message_id=main_message_id,
            reply_markup=get_subjects_markup(res),
        )


# | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject | GetSubject |


@dp.callback_query_handler(
    state=StudentAddHomework.GetSubjects, text_contains="subject"
)
async def query_get_sunject(callback: CallbackQuery):
    await callback.answer()
    subject = callback.data.split(":")[1]
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["subject"] = subject
        await StudentAddHomework.WaitHomework.set()
        main_message_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.send_homework, callback),
            chat_id=chat_id,
            message_id=main_message_id,
            reply_markup=markup_done,
        )


# | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add | Fast Add |


@dp.callback_query_handler(state=StudentAddHomework.FastAdd, text_contains="subject")
async def query_get_subject(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        FSMdata["subject"] = callback.data.split(":")[1]
        await StudentAddHomework.WaitHomework.set()
        main_message_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.send_homework, callback),
            chat_id=chat_id,
            message_id=main_message_id,
            reply_markup=markup_done,
        )


# | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework | WaitHomework |


@dp.message_handler(
    StudentFilter(),
    state=StudentAddHomework.WaitHomework,
    content_types=ContentType.ANY,
)
async def hanldler_wait_homework(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if msg.text or msg.caption:
            FSMdata["text"] = f"{FSMdata['text']}\n{(msg.text or msg.caption)}".lstrip()
        if msg.photo:
            FSMdata["files_tgid"].append(msg.photo[-1].file_id)


@dp.callback_query_handler(state=StudentAddHomework.WaitHomework, text="done")
async def query_homework_check(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if len(FSMdata["text"]) == 0 and len(FSMdata["files_tgid"]) == 0:
            await callback.message.answer(process_text(TextKeys.no_hw, callback))
        else:
            await StudentAddHomework.CheckHomework.set()
            await callback.message.answer(
                process_text(TextKeys.check_hw, callback, subject=FSMdata["subject"]),
                reply_markup=markup_check_homework,
            )


# | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework | CheckHomework |


@dp.callback_query_handler(
    state=StudentAddHomework.CheckHomework,
    text_contains="check_homework",
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
            await add_homework(userid, params, auto=FSMdata["is_fast"])
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    msg = await callback.message.answer(
        process_text(TextKeys.menu, callback),
        reply_markup=get_markup_student_menu(True),
    )
    async with FSMContext.proxy() as FSMdata:
        FSMdata["main_msg_id"] = msg.message_id
