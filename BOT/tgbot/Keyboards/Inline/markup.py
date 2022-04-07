from distutils.command import check
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

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
