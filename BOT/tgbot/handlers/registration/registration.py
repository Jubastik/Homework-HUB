from aiogram.types import CallbackQuery, Message, User
from CONSTANTS import SUBJECTS, TG_BOT_LINK, TG_OFFICAL_CHANNEL
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.filters import RegistrationFilter
from tgbot.FSM.states import RegistrationStates, StudentMenu

from tgbot.keyboards.inline.markup import (
    get_markup_shedule,
    get_markup_student_menu,
    markup_check_subjects1,
    markup_shedule2,
    markup_start,
    markup_yes_or_no,
    markup_back,
)
from tgbot.services.restapi.restapi import (
    get_student_info,
    is_admin,
    register_class,
    register_user,
)
from tgbot.services.scripts import (
    convert_time,
    make_username,
    time_is_correct,
    parse_args,
)
from tgbot.handlers.shortcuts import back_to_registration_menu
from tgbot.handlers.registration.registration_manager import RegistrationManager
from tgbot.services.sub_classes import RestErorr, SheduleData

from bot import bot, dp


@dp.message_handler(RegistrationFilter(), commands=["start"], state="*")
async def registration_menu(msg: Message):  # on /start in registration state
    # !Обработка deeplinking
    # пример: t.me/YandexLyceum_rulka_bot?start=94811
    await msg.delete()
    userid = msg.from_user.id
    FSMContext = dp.current_state(user=userid)
    await FSMContext.reset_state()
    # DeepLinking registration
    if args := msg.get_args():
        args = parse_args(args)
        if class_id := args.get("start"):
            # often user hasn't @username and we have to take first_name and last_name
            username = make_username(User.get_current())
            res = await register_user(userid, class_id, username)
            if isinstance(res, RestErorr):
                await FSMContext.reset_state()
                return
            await msg.answer(process_text(TextKeys.by_link_success, msg))
            res = await is_admin(msg.from_user.id)
            if isinstance(res, RestErorr):
                await FSMContext.reset_state()
                return
            await StudentMenu.Menu.set()
            msg = await msg.answer(
                process_text(TextKeys.menu, msg),
                reply_markup=get_markup_student_menu(res),
            )
            async with FSMContext.proxy() as FSMdata:
                FSMdata["main_msg_id"] = msg.message_id
            return

    # Regular registration
    await msg.answer(process_text(TextKeys.warning, msg))
    async with FSMContext.proxy() as FSMdata:
        # Запуск регистрации
        rm = RegistrationManager(msg)
        await rm.init_registration(msg)
        FSMdata["registration_manager"] = rm
    await RegistrationStates.StartBtn.set()


@dp.callback_query_handler(RegistrationFilter(), state=RegistrationStates.StartBtn)
async def handle_start_query(callback: CallbackQuery):
    FSMcontext = dp.current_state(user=callback.from_user.id)
    async with FSMcontext.proxy() as FSMdata:
        rm = FSMdata["registration_manager"]
        await rm.on_callback(callback)


@dp.message_handler(RegistrationFilter(), state=RegistrationStates.StartBtn)
async def handle_start_message(msg: Message):
    FSMcontext = dp.current_state(user=msg.from_user.id)
    async with FSMcontext.proxy() as FSMdata:
        rm = FSMdata["registration_manager"]
        await rm.on_message(msg)


# # By class token registration
# @dp.callback_query_handler(
#     RegistrationFilter(), state=RegistrationStates.StartBtn, text="join_class_by_id"
# )
# async def query_join_class(callback: CallbackQuery):  # on /start/присоединиться
#     await callback.answer()
#     await RegistrationStates.GetGroupId.set()
#     FSMContext = dp.current_state(user=callback.from_user.id)
#     async with FSMContext.proxy() as FSMdata:
#         main_msg_id = FSMdata["main_msg_id"]
#         chat_id = callback.from_user.id
#     await bot.edit_message_text(
#         process_text(TextKeys.get_class_token, callback),
#         chat_id=chat_id,
#         message_id=main_msg_id,
#         reply_markup=markup_back,
#     )


# @dp.callback_query_handler(
#     RegistrationFilter(),
#     state=[RegistrationStates.GetGroupId, RegistrationStates.CheckStartTime],
#     text="back",
# )
# async def back_to_menu(
#     callback: CallbackQuery,
# ):  # on /start/присоединиться/назад or /start/создать класс/назад
#     await back_to_registration_menu(callback)
#     await RegistrationStates.StartBtn.set()


# @dp.message_handler(RegistrationFilter(), state=RegistrationStates.GetGroupId)
# async def handler_get_id(msg: Message):  # on /start/присоединиться/<message>
#     await msg.delete()
#     classid = msg.text
#     userid = msg.from_user.id
#     # often user hasn't @username and we have to take first_name and last_name
#     username = make_username(User.get_current())
#     FSMContext = dp.current_state(user=userid)
#     res = await register_user(userid, classid, username)
#     if isinstance(res, RestErorr):
#         await FSMContext.reset_state()
#         return
#     await StudentMenu.Menu.set()
#     res = await is_admin(msg.from_user.id)
#     if isinstance(res, RestErorr):
#         return
#     async with FSMContext.proxy() as FSMdata:
#         main_msg_id = FSMdata["main_msg_id"]
#     message = await bot.edit_message_text(
#         process_text(TextKeys.menu, msg),
#         chat_id=userid,
#         message_id=main_msg_id,
#         reply_markup=get_markup_student_menu(res),
#     )
#     # Сброс состояния, в связи с переходом завершением регистрации
#     await FSMContext.reset_state()
#     async with FSMContext.proxy() as FSMdata:
#         FSMdata["main_msg_id"] = message.message_id


# # Make new class registration
# @dp.callback_query_handler(
#     RegistrationFilter(), state=RegistrationStates.StartBtn, text="make_class"
# )
# async def query_new_class(callback: CallbackQuery):  # on /start/создать класс
#     await callback.answer()
#     FSMContext = dp.current_state(user=callback.from_user.id)
#     async with FSMContext.proxy() as FSMdata:  # Создание дефолтной FSMdata
#         time = FSMdata["start_time"] = ["9", "00"]
#         main_msg_id = FSMdata["main_msg_id"]
#         FSMdata["extra_subjects"] = []
#         FSMdata["shedule"] = SheduleData()
#         FSMdata["current_pos"] = 0
#     await RegistrationStates.CheckStartTime.set()
#     await bot.edit_message_text(
#         process_text(
#             TextKeys.start_time_check,
#             callback,
#             time=":".join(convert_time(time)),
#         ),
#         chat_id=callback.from_user.id,
#         message_id=main_msg_id,
#         reply_markup=markup_yes_or_no,
#     )