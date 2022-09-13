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


class StudentAddHomework(StatesGroup):
    # Ветка AddHomework
    AddHomework = State()
    FastAdd = State()

    GetDate = State()
    GetSubjects = State()

    WaitHomework = State()  # общий для FastAdd и Add
    CheckHomework = State()  # общий для FastAdd и Add


class StudentProfile(StatesGroup):
    # Ветка Profile
    Profile = State()
    Shedule = State()
    DeleteAccount = State()


class StudentMenu(StatesGroup):
    # Менюшка
    Menu = State()


class StudentClass(StatesGroup):
    # Ветка панели управления классом
    ClassPanel = State()
    AddAdmin = State()
    KickClassmate = State()


class StudentGetHomework(StatesGroup):
    # Ветка полечения домашки
    GetHomework = State()
    GetDate = State()


class Developer(StatesGroup):
    # Состояния разработчика
    Panel = State()
    MailingGetText = State()
    MailingCheck = State()


class Group(StatesGroup):
    # Состояния группы
    Menu = State()
    GetHomework = State()
    GetDate = State()