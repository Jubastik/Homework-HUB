from aiogram.types import CallbackQuery
from aiogram.dispatcher import FSMContext

from BOT.bot import dp
from BOT.tgbot.handlers.student.menu import query_profile
from BOT.tgbot.FSM.states import StudentProfile
from BOT.tgbot.filters.student_filter import StudentFilter
from BOT.tgbot.services.sub_classes import RestErorr
from BOT.tgbot.keyboards.inline.markup import markup_are_u_sure
from BOT.tgbot.services.restapi.restapi import delete_user


@dp.callback_query_handler(
    StudentFilter(), state=StudentProfile.Profile, text="delete_account"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    await StudentProfile.DeleteAccount.set()
    await callback.message.answer(
        "Вы уверены что хотите удалить аккаунт?", reply_markup=markup_are_u_sure
    )


# | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount | DeleteAccount |


@dp.callback_query_handler(
    StudentFilter(), state=StudentProfile.DeleteAccount, text="true"
)
async def query_get_homework(callback: CallbackQuery):
    await callback.answer()
    FSMContext = dp.current_state(user=callback.from_user.id)
    res = await delete_user(callback.from_user.id)
    if isinstance(res, RestErorr):
        await FSMContext.reset_state()
        return
    await callback.message.answer("Ваш аккаунт удалён")
    await FSMContext.reset_state()
    # Соединение с регистрацией...


@dp.callback_query_handler(
    StudentFilter(), state=StudentProfile.DeleteAccount, text="false"
)
async def query_get_homework(callback: CallbackQuery):
    await query_profile(callback)
