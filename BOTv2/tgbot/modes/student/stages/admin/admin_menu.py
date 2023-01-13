from aiogram.types import CallbackQuery

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_class_panel,
)

from services.restapi.restapi import get_user, get_class
from services.restapi.api_error import ApiError


class AdminMenu(Stage):
    def __init__(self, mode):
        super().__init__(mode)
        self.text = lambda *args, status="", **kwargs: process_text(TextKeys.class_panel, status=status, **kwargs)
        self.markup = markup_class_panel
