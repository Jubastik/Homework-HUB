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
    # 3) Получение расписания
    AddShedule = State()  # Форма заполнения
    # 4) Проверка
    IsCorrect = State()


class StudentStates(StatesGroup):
    """Состояния студента и админа"""
    # General
    StudentMenu = State()

    # StudentMenu
    Profile = State()
    ClassPanel = State()
    AddHomework = State()
    GetHomework = State()

    # Ветка AddHomework
    FastAdd = State()
    Add = State()
    WaitHomework = State()  # общий для FastAdd и Add
    CheckHomework = State()


