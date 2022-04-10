from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher import FSMContext
from emoji import emojize

from CONSTANTS import SUBJECTS
from tgbot.Keyboards.Inline.CallbackData import SubjectData, ArrowsData

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
        [InlineKeyboardButton(text="Отмена", callback_data="Check_Subjects_undo")],
    ]
)
Shedule2_markup = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Готово", callback_data="shedule_done")]
    ]
)


def get_SheduleMarkup(subjects):
    keyboard = InlineKeyboardMarkup(row_width=3)
    for i in range(len(subjects)):
        keyboard.insert(
            InlineKeyboardButton(
                text=subjects[i],
                callback_data=SubjectData.new(name=subjects[i]),
            )
        )
    keyboard.add(
        InlineKeyboardButton(text="Вверх", callback_data=ArrowsData.new(num=-1)),
        InlineKeyboardButton(text="Вниз", callback_data=ArrowsData.new(num=1)),
    )
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data="back"))
    return keyboard
