from aiogram import Dispatcher

from .admin import register_admin_handlers
from .developer import register_developer_handlers
from .registration import register_registration_handlers
from .student import register_student_handlers


def setup(dp: Dispatcher):
    register_admin_handlers(dp)
    register_developer_handlers(dp)
    register_registration_handlers(dp)
    register_student_handlers(dp)
