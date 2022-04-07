from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """Состояния регистрации"""

    # Вход:
    Start = State()
    GetGroupId = State()
    # Создание класса:
    # 1) Получение времени старта уроков
    GetStartTime = State()  # "Уроки начинаются в 9:00?"
    GetOtherTime = State()  # Если уроки не в 9:00
    # 2) Получение списка предметов класса
    CheckSubjects = State()
    AddSubject = State()
    CheckSubjectsAgain = State()
    # 3) Получение кол-ва уроков каждый день

    # 4) Получение расписания



class GetHomeworkStates(StatesGroup):
    pass


# Этого класса должно быть несколько типов, тк мы можем добавлять "дз на дату"
class AddHomeworkStates(StatesGroup):
    pass


class RemoveHomeworkStates(StatesGroup):
    pass
