"""
Коды ошибок для Homework HUB
Первые 2 цифры - место ошибки
Вторые 2 цифры - номер ошибки

Описание первых 2 цифр:ё
10: Ошибка валидации
11: ошибка ученика
12: ошибка класса
13: ошибка расписания
"""


class APIError(Exception):
    def __init__(self, status_code: int, err_id: int, msg: str):
        self.msg = msg
        self.status_code = status_code
        self.err_id = err_id


VALIDATION_ERROR = 1000

STUDENT_NOT_FOUND = 1100
STUDENT_NOT_IN_CLASS = 1101
STUDENT_BAN_IN_CLASS = 1102
STUDENT_INIT_INVALID_DATA = 1103

CLASS_NOT_FOUND = 1201
INVALID_CLASS_TOKEN = 1202

SLOT_NOT_FOUND = 1301
