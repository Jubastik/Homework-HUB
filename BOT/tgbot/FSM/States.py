from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """Состояния регистрации"""

    # Вход:
    StartBtn = State()
    GetGroupId = State()
    # Создание класса:
    # 1) Получение времени старта уроков
    CheckStartTime = State()  # "Уроки начинаются в 9:00?"
    AddTime = State()  # Если уроки не в 9:00
    # 2) Получение списка предметов класса
    CheckSubjects = State()  # Все ли предметы есть в списке?
    # AddSubject = State()  # Добавить предмет в список
    # CheckSubjectsAgain = State()  # Все ли предметы есть в списке? (по другому)
    # 3) Получение расписания
    AddShedule = State()  # Форма заполнения
    # 4) Проверка
    IsCorrect = State()


class GetHomeworkStates(StatesGroup):
    pass


# Этого класса должно быть несколько типов, тк мы можем добавлять "дз на дату"
class AddHomeworkStates(StatesGroup):
    pass


class RemoveHomeworkStates(StatesGroup):
    pass
