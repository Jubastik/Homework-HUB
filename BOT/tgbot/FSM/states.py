from aiogram.dispatcher.filters.state import StatesGroup, State


class RegistrationStates(StatesGroup):
    """Состояния регистрации"""

    # Вход:
    GetGroupId = State()
    # Создание класса:
    # ...


class GetHomeworkStates(StatesGroup):
    pass


# Этого класса должно быть несколько типов, тк мы можем добавлять "дз на дату"
class AddHomeworkStates(StatesGroup):
    pass


class RemoveHomeworkStates(StatesGroup):
    pass
