from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """Состояния регистрации"""

    # Вход:
    StartBtn = State()
    GetGroupId = State()
    # Создание класса:
    # 1) Получение времени старта уроков
    GetStartTime = State()  # "Уроки начинаются в 9:00?"
    GetOtherTime = State()  # Если уроки не в 9:00
    # 2) Получение списка предметов класса
    CheckSubjects = State()  # Все ли предметы есть в списке?
    AddSubject = State()  # Добавить предмет в список
    CheckSubjectsAgain = State()  # Все ли предметы есть в списке? (по другому)
    # 4) Получение расписания
    Form = State()  # Форма заполнения


class GetHomeworkStates(StatesGroup):
    pass


# Этого класса должно быть несколько типов, тк мы можем добавлять "дз на дату"
class AddHomeworkStates(StatesGroup):
    pass


class RemoveHomeworkStates(StatesGroup):
    pass
