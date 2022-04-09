from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext

from CONSTANTS import SUBJECTS

# InlineKeyboardMarkup - кнопочки

Start_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Присоединиться к классу по id", callback_data="join_class_by_id"
            ),
            InlineKeyboardButton(text="Создать класс", callback_data="make_class"),
        ],
    ]
)

YesOrNo_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="check_true"),
            InlineKeyboardButton(text="Нет", callback_data="check_false"),
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
)

CheckSubjects1_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всё верно", callback_data="Check_Subjects_okey")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
)
CheckSubjects2_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Вернуть", callback_data="Check_Subjects_undo")],
    ]
)


def get_FormMarkup(FSMContext: FSMContext):
    inline_keyboard = [[], [InlineKeyboardButton(text="Назад", callback_data="back")]]
    return InlineKeyboardMarkup()
