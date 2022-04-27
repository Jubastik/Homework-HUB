from aiogram.types import CallbackQuery

from bot import dp
from tgbot.FSM.states import (
    StudentClass,
)
from tgbot.filters.student_filter import StudentFilter
from tgbot.filters.admin_filter import AdminFilter
from tgbot.keyboards.inline.markup import get_markup_classmates, markup_class_panel
from tgbot.services.restapi.restapi import (
    get_names_classmates,
    delete_user,
    assign_admin,
    change_class_token,
)
from tgbot.services.sub_classes import RestErorr
from tgbot.services.scripts import convert_users


async def send_panel(callback: CallbackQuery):
    res = await get_names_classmates(callback.from_user.id)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    txt = convert_users(res)
    await callback.message.answer(
        txt, reply_markup=markup_class_panel
    )



@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentClass.ClassPanel, text="add_admin"
)
async def query_add_admin(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.AddAdmin.set()
    res = await get_names_classmates(callback.from_user.id)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await callback.message.answer(
        "Выберете одноклассника:", reply_markup=get_markup_classmates(res)
    )


@dp.callback_query_handler(
    StudentFilter(),
    AdminFilter(),
    state=StudentClass.AddAdmin,
    text_contains="student_name",
)
async def query_add_admin(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")[1]
    res = await assign_admin(data)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await StudentClass.ClassPanel.set()
    await send_panel(callback)

@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentClass.ClassPanel, text="kick"
)
async def query_kick(callback: CallbackQuery):
    await callback.answer()
    await StudentClass.KickClassmate.set()
    res = await get_names_classmates(callback.from_user.id)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await callback.message.answer(
        "Выберете одноклассника:", reply_markup=get_markup_classmates(res)
    )


@dp.callback_query_handler(
    StudentFilter(),
    AdminFilter(),
    state=StudentClass.KickClassmate,
    text_contains="student_name",
)
async def query_delete_user(callback: CallbackQuery):
    await callback.answer()
    data = callback.data.split(":")[1]
    res = await delete_user(data)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return


@dp.callback_query_handler(
    StudentFilter(), AdminFilter(), state=StudentClass.ClassPanel, text="remove_token"
)
async def query_remove_token(callback: CallbackQuery):
    await callback.answer()
    res = await change_class_token(callback.from_user.id)
    if isinstance(res, RestErorr):
        FSMContext = dp.current_state(user=callback.from_user.id)
        await FSMContext.reset_state()
        return
    await send_panel(callback)


# 1) [{tg_id: student_name}]
# 2) {name: str, is_admin: Bool, class_token: int, admins: [str, str]}
# 3) str
