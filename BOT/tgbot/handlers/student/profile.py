from aiogram.types import CallbackQuery

from bot import dp, bot
from tgbot.handlers.student.menu import query_profile
from tgbot.FSM.states import StudentProfile
from tgbot.filters.student_filter import StudentFilter
from tgbot.services.sub_classes import RestErorr
from tgbot.keyboards.inline.markup import markup_are_u_sure, markup_get_shedule
from tgbot.services.restapi.restapi import delete_user, get_shedule
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


@dp.callback_query_handler(state=StudentProfile.Profile, text="delete_account")
async def query_delete_watning(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentProfile.DeleteAccount.set()
    async with FSMContext.proxy() as FSMdata:
        main_msg_id = FSMdata["main_msg_id"]
        chat_id = callback.from_user.id
        await bot.edit_message_text(
            process_text(TextKeys.delete_account, callback),
            chat_id=chat_id,
            message_id=main_msg_id,
            reply_markup=markup_are_u_sure,
        )


# | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount |


@dp.callback_query_handler(state=StudentProfile.DeleteAccount, text="true")
async def query_delete_true(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await delete_user(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await callback.message.answer("Ваш аккаунт удалён")
    await FSMContext.reset_state()
    # Соединение с регистрацией...


@dp.callback_query_handler(state=StudentProfile.DeleteAccount, text="false")
@dp.callback_query_handler(state=StudentProfile.Shedule, text="back")
async def query_delete_false(callback: CallbackQuery):
    await query_profile(callback)


# | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule | GetShedule |


@dp.callback_query_handler(state=StudentProfile.Profile, text="get_shedule")
async def query_delete_true(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    await StudentProfile.Shedule.set()
    res = await get_shedule(callback.from_user.id)
    async with FSMContext.proxy() as FSMdata:
        msgid = FSMdata["main_msg_id"]
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await bot.edit_message_text(
        process_text(
            TextKeys.shedule3,
            callback,
            **res.get_formatted_shedule(),
        ),
        chat_id=callback.message.chat.id,
        message_id=msgid,
        reply_markup=markup_get_shedule,
    )
