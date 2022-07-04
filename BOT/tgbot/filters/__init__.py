from aiogram import Dispatcher

from .admin_filter import AdminFilter
from .developer_filter import DeveloperFilter
from .registration_filter import RegistrationFilter
from .student_filter import StudentFilter
from .group_filter import GroupFilter, IsRegisteredGroupFilter, RegistrationGroupFilter


def setup(dp: Dispatcher):
    dp.filters_factory.bind(AdminFilter)
    dp.filters_factory.bind(DeveloperFilter)
    dp.filters_factory.bind(RegistrationFilter)
    dp.filters_factory.bind(StudentFilter)
    dp.filters_factory.bind(GroupFilter)
    dp.filters_factory.bind(IsRegisteredGroupFilter)
    dp.filters_factory.bind(RegistrationGroupFilter)
