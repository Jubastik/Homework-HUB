from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


# InlineKeyboardMarkup - кнопочки

empty_markup = InlineKeyboardMarkup()


start_on = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Присоединиться к классу по id", callback_data="join_class_by_id"
            ),
            InlineKeyboardButton(text="Создать класс", callback_data="make_class"),
        ],
    ]
)
