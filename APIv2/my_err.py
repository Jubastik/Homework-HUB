"""
Коды ошибок для Homework HUB
Первые 2 цифры - место ошибки
Вторые 2 цифры - номер ошибки

Описание первых 2 цифр:
3х значные - HTTP код ошибки
10: Ошибка валидации
11: ошибка ученика
12: ошибка класса
13: ошибка расписания
15: ошибки парсера
"""


class APIError(Exception):
    def __init__(self, status_code: int, err_id: int, msg: str):
        self.msg = msg
        self.status_code = status_code
        self.err_id = err_id


INTERNAL_SERVER_ERROR = 500

VALIDATION_ERROR = 1000
INVALID_ROOT_TOKEN = 1001
IN_DEVELOPMENT = 1002

STUDENT_NOT_FOUND = 1100
STUDENT_NOT_IN_CLASS = 1101
STUDENT_BAN_IN_CLASS = 1102
STUDENT_INIT_INVALID_DATA = 1103
STUDENT_ALREADY_EXISTS = 1104

CLASS_NOT_FOUND = 1201
INVALID_CLASS_TOKEN = 1202
UPDATE_CLASS_INVALID_DATA = 1203

SLOT_NOT_FOUND = 1301
HOMEWORK_NO_SUCH_LESSON = 1302

ParserNotActive = 1500
ParserNotFound = 1501
ParserLoginError = 1502
ParserAccessError = 1503

