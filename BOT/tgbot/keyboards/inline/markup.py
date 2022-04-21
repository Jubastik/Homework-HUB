from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from BOT.CONSTANTS import SUBJECTS
from BOT.tgbot.keyboards.inline.callback_data import SubjectData, ArrowsData, CheckHomework


# | Registration | Registration | Registration | Registration | Registration | Registration | Registration | Registration |


markup_start = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Присоединиться к классу по id", callback_data="join_class_by_id"
            ),
            InlineKeyboardButton(text="Создать класс", callback_data="make_class"),
        ],
    ]
)

markup_yes_or_no = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="check_true"),
            InlineKeyboardButton(text="Нет", callback_data="check_false"),
        ],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
)

markup_check_subjects1 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Всё верно", callback_data="Check_Subjects_okey")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]
)
markup_check_subjects2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="Check_Subjects_undo")],
    ]
)
markup_shedule2 = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Готово", callback_data="shedule_done")]
    ]
)


def get_markup_shedule(subjects) -> InlineKeyboardMarkup:
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


# | Student | Student | Student | Student | Student | Student | Student | Student |


markup_profile = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
        [InlineKeyboardButton(text="Удалить аккаунт", callback_data="delete_account")],
    ]
)

markup_add_homework = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Быстро добавить", callback_data="fast_add")],
        [InlineKeyboardButton(text="Добавить на дату", callback_data="on_date")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
    ]
)


def get_markup_student_menu(is_admin) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Добавить дз📌", callback_data="add_homework"),
                InlineKeyboardButton(text="Получить дз🔍", callback_data="get_homework"),
            ],
            [InlineKeyboardButton(text="Профиль👤", callback_data="profile")],
        ]
    )
    if is_admin:
        keyboard.add(InlineKeyboardButton(text="Класс⭐️", callback_data="class_menu"))

    return keyboard


def get_markup_fast_add1(subjects) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=subjects[0], callback_data=SubjectData.new(name=subjects[0])
                )
            ],
            [
                InlineKeyboardButton(
                    text=subjects[1], callback_data=SubjectData.new(name=subjects[1])
                )
            ],
            [InlineKeyboardButton(text="Меню", callback_data="menu")],
        ]
    )
    return keyboard


markup_check_homework = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Да, все верно", callback_data=CheckHomework.new(boolean="true")
            )
        ],
        [
            InlineKeyboardButton(
                text="Нет", callback_data=CheckHomework.new(boolean="false")
            )
        ],
    ]
)
markup_done = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Готово", callback_data="done")],
        [InlineKeyboardButton(text="Меню", callback_data="menu")],
    ]
)

# keyboard = InlineKeyboardMarkup(
#     inline_keyboard=[
#         [InlineKeyboardButton(text="Среда 20.04", callback_data="add_homework"), InlineKeyboardButton(text="Суббота 23.04", callback_data="add_homework")],
#         [InlineKeyboardButton(text="Четверг 21.04", callback_data="add_homework"), InlineKeyboardButton(text="Понедельник 25.04", callback_data="add_homework")],
#         [InlineKeyboardButton(text="Пятница 22.04", callback_data="add_homework"), InlineKeyboardButton(text="Вторник 26.04", callback_data="add_homework")],
#     ]
# )
