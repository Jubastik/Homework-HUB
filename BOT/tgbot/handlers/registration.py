from aiogram.types import Message, CallbackQuery, User


# | start | start | start | start | start | start | start | start |
from CONSTANTS import SUBJECTS
from bot import dp, bot
from tgbot.FSM.states import RegistrationStates, StudentMenu
from tgbot.filters import RegistrationFilter
from tgbot.keyboards.inline.markup import (
    markup_yes_or_no,
    markup_check_subjects1,
    markup_start,
    markup_check_subjects2,
    get_markup_shedule,
    markup_shedule2,
    get_markup_student_menu,
)
from tgbot.services.restapi.restapi import register_user, register_class, is_admin
from tgbot.services.scripts import convert_time, time_is_correct, convert_position
from tgbot.services.sub_classes import RestErorr, SheduleData


@dp.message_handler(RegistrationFilter(), commands=["start"], state="*")
async def hanldler_start(msg: Message):
    # !Обработка deeplinking
    # пример: t.me/YandexLyceum_rulka_bot?start=class_token94811
    # print(msg.text)
    if len(msg.text.split()) == 2:
        classid = msg.text.split()[-1]
        userid = msg.from_user.id
        username = User.get_current()["username"]
        FSMContext = dp.current_state(user=userid)
        res = await register_user(userid, classid, username)
        if isinstance(res, RestErorr):
            await FSMContext.reset_state()
            return
        await msg.answer(
            "Регистрация по ссылке успешна"
        )  # Тут надо сделать отправку менюшки студента
        res = await is_admin(msg.from_user.id)
        if isinstance(res, RestErorr):
            return
        await FSMContext.reset_state()
        await StudentMenu.Menu.set()
        await msg.answer(
            "Меню",
            reply_markup=get_markup_student_menu(res),
        )
    else:
        FSMContext = dp.current_state(user=msg.from_user.id)
        await FSMContext.reset_state()
        await msg.answer(
            "Привет!!! Я бот для быстрого сохранения домашки", reply_markup=markup_start
        )
        await RegistrationStates.StartBtn.set()


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.StartBtn, text="make_class"
)
async def query_new_class(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:  # Создание дефолтной FSMdata
        time = FSMdata["start_time"] = ["9", "00"]
        FSMdata["extra_subjects"] = []
        FSMdata["shedule"] = SheduleData()
        FSMdata["current_pos"] = 0
    await RegistrationStates.CheckStartTime.set()
    await callback.message.answer(
        f"Ваши уроки начинаются в {' : '.join(convert_time(time))}?",
        reply_markup=markup_yes_or_no,
    )


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.StartBtn, text="join_class_by_id"
)
async def query_join_class(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.GetGroupId.set()
    await callback.message.answer(
        "Введите id класса. Его можно получить у участника класса."
    )


# | GetGroupId | GetGroupId | GetGroupId | GetGroupId | GetGroupId | GetGroupId | GetGroupId | GetGroupId |


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.GetGroupId)
async def handler_get_id(msg: Message):
    classid = msg.text
    userid = msg.from_user.id
    username = User.get_current()["username"]
    FSMContext = dp.current_state(user=userid)
    res = await register_user(userid, classid, username)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await FSMContext.reset_state()
    await StudentMenu.Menu.set()
    res = await is_admin(msg.from_user.id)
    if isinstance(res, RestErorr):
        return
    await msg.answer(
        "Меню",
        reply_markup=get_markup_student_menu(res),
    )


# | CheckStartTime | CheckStartTime | CheckStartTime | CheckStartTime | CheckStartTime | CheckStartTime | CheckStartTime | CheckStartTime |


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckStartTime, text="check_true"
)
async def query_check_start_time_true(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await RegistrationStates.CheckSubjects.set()
    async with FSMContext.proxy() as FSMdata:
        subjects_msg = await callback.message.answer(
            "\n".join(
                [
                    "Предметы:",
                    *SUBJECTS,
                    *FSMdata["extra_subjects"],
                ]
            )
        )
        await callback.message.answer(
            "\n".join(
                [
                    "Есть ли тут все ваши школьные предметы?",
                    "Если нет - отправьте название предмета, который хотите добавить в список",
                ]
            ),
            reply_markup=markup_check_subjects1,
        )
        subjects_msg_id = subjects_msg.message_id
        FSMdata["subjects_msg_id"] = subjects_msg_id


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckStartTime, text="check_false"
)
async def query_check_start_time_false(callback: CallbackQuery):
    await callback.answer()
    await RegistrationStates.AddTime.set()
    await callback.message.answer(
        'Введите время начала уроков в формате: "часы:минуты"\nНапример 8:30'
    )


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckStartTime, text="back"
)
async def query_check_start_time_back(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("Способы регистрации:", reply_markup=markup_start)
    await RegistrationStates.StartBtn.set()


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.AddTime)
async def handler_add_time(msg: Message):
    time = msg.text
    FSMContext = dp.current_state(user=msg.from_user.id)
    if time_mod := time_is_correct(time):
        await msg.answer(
            f'Записано время начала уроков: "{" : ".join(convert_time(time_mod))}"'
        )  # Для тестов
        async with FSMContext.proxy() as FSMdata:
            FSMdata["start_time"] = time_mod
            subjects_msg = await msg.answer(
                "\n".join(
                    [
                        "Предметы:",
                        *SUBJECTS,
                        *FSMdata["extra_subjects"],
                    ]
                )
            )
            await msg.answer(
                "\n".join(
                    [
                        "Есть ли тут все ваши школьные предметы?",
                        "Если нет - отправьте название предмета, который хотите добавить в список",
                    ]
                ),
                reply_markup=markup_check_subjects1,
            )
            FSMdata["subjects_msg_id"] = subjects_msg.message_id
            await RegistrationStates.CheckSubjects.set()
    else:
        await msg.answer("Время введено некорректно, попробуйте ещё раз")


# | CheckSubjects | CheckSubjects | CheckSubjects | CheckSubjects | CheckSubjects | CheckSubjects | CheckSubjects | CheckSubjects |


@dp.callback_query_handler(
    RegistrationFilter(), state=RegistrationStates.CheckSubjects, text="back"
)
async def query_check_subjects_back(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        await RegistrationStates.CheckStartTime.set()
        await callback.message.answer(
            f"Ваши уроки начинаются в {' : '.join(convert_time(FSMdata['start_time']))}?",
            reply_markup=markup_yes_or_no,
        )


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.CheckSubjects,
    text="Check_Subjects_undo",
)
async def query_check_subjects_undo(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        if len(FSMdata["extra_subjects"]) > len(SUBJECTS):
            FSMdata["extra_subjects"] = FSMdata["extra_subjects"][:-1]
            msgid = FSMdata["subjects_msg_id"]
            await bot.edit_message_text(
                "\n".join(
                    [
                        "Предметы:",
                        *SUBJECTS,
                        *FSMdata["extra_subjects"],
                    ]
                ),
                chat_id=callback.message.chat.id,
                message_id=msgid,
                reply_markup=markup_check_subjects2,
            )


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.CheckSubjects)
async def handler_add_subject(msg: Message):
    FSMContext = dp.current_state(user=msg.from_user.id)
    subject = msg.text
    async with FSMContext.proxy() as FSMdata:
        FSMdata["extra_subjects"].append(subject)
        msgid = FSMdata["subjects_msg_id"]
        await bot.edit_message_text(
            "\n".join(
                [
                    "Предметы:",
                    *SUBJECTS,
                    *FSMdata["extra_subjects"],
                ]
            ),
            chat_id=msg.chat.id,
            message_id=msgid,
            reply_markup=markup_check_subjects2,
        )


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.CheckSubjects,
    text="Check_Subjects_okey",
)
async def query_check_subjects_undo(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        msg = await callback.message.answer(
            "\n".join(
                [
                    "Расписание:",
                    *FSMdata["shedule"].get_readable_shedule(
                        current_id=convert_position(FSMdata["current_pos"])
                    ),
                ]
            )
        )
        FSMdata["shedule_msg_id"] = msg.message_id
        await RegistrationStates.AddShedule.set()
        await callback.message.answer(
            "\n".join(
                [
                    "Давай заполним расписание",
                    "P.s. Ожидайте, пока на кнопках будут часики и только потом нажимайте следующую кнопку",
                ]
            ),
            reply_markup=get_markup_shedule([*SUBJECTS, *FSMdata["extra_subjects"]]),
        )


# | AddShedule | AddShedule | AddShedule | AddShedule | AddShedule | AddShedule | AddShedule | AddShedule |


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.AddShedule,
    text_contains="up_or_down",
)
async def query_move_cursor(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    move_num = int(callback.data.split(":")[1])
    async with FSMContext.proxy() as FSMdata:
        if 0 <= (FSMdata["current_pos"] + move_num) <= 47:
            FSMdata["current_pos"] += move_num
            pos = convert_position(FSMdata["current_pos"])
            msgid = FSMdata["shedule_msg_id"]
            await bot.edit_message_text(
                "\n".join(
                    [
                        "Расписание:",
                        *FSMdata["shedule"].get_readable_shedule(current_id=pos),
                    ]
                ),
                chat_id=callback.message.chat.id,
                message_id=msgid,
                reply_markup=markup_shedule2,
            )


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.AddShedule,
    text_contains="subject",
)
async def query_add_shedule(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        subject = callback.data.split(":")[1]
        msgid = FSMdata["shedule_msg_id"]
        pos = convert_position(FSMdata["current_pos"])
        FSMdata["shedule"].add_lesson(subject, pos)
        if FSMdata["current_pos"] + 1 <= 47:
            FSMdata["current_pos"] += 1
            pos = convert_position(FSMdata["current_pos"])
        await bot.edit_message_text(
            "\n".join(
                [
                    "Расписание:",
                    *FSMdata["shedule"].get_readable_shedule(current_id=pos),
                ]
            ),
            chat_id=callback.message.chat.id,
            message_id=msgid,
            reply_markup=markup_shedule2,
        )


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.AddShedule,
    text="shedule_done",
)
async def query_shedule_done(callback: CallbackQuery):
    await callback.answer()
    userid = callback.from_user.id
    FSMContext = dp.current_state(user=userid)
    async with FSMContext.proxy() as FSMdata:
        data = {
            "shedule": FSMdata["shedule"],
            "subjects": FSMdata["extra_subjects"],
            "start_time": FSMdata["start_time"],
            "user_name": User.get_current()["username"],
        }
        res = await register_class(userid, data)
        if isinstance(res, RestErorr):
            await FSMContext.reset_state()
            return
        await FSMContext.reset_state()
        await callback.message.answer("Регистрация успешна")
        res = await is_admin(callback.from_user.id)
        if isinstance(res, RestErorr):
            return
        await StudentMenu.Menu.set()
        await callback.message.answer(
            "Меню",
            reply_markup=get_markup_student_menu(res),
        )


@dp.callback_query_handler(
    RegistrationFilter(),
    state=RegistrationStates.AddShedule,
    text="back",
)
async def query_add_shedule_back(callback: CallbackQuery):
    await query_check_start_time_true(callback)
