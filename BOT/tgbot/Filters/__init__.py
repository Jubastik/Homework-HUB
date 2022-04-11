from aiogram import Dispatcher

from .AdminFilter import AdminFilter
from .DeveloperFilter import DeveloperFilter
from .RegistrationFilter import RegistrationFilter
from .StudentFilter import StudentFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(DeveloperFilter)
    dp.filters_factory.bind(RegistrationFilter)
    dp.filters_factory.bind(StudentFilter)
