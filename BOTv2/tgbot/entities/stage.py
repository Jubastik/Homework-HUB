from aiogram.types import CallbackQuery, Message


class Stage:  # Abstract class
    name = "entry_stage"

    def __init__(self, mode):
        self.mode = mode
        self.user = mode.user
        self.text = lambda *args, **kwargs: "No activate method"

    async def activate(self, **kwargs) -> int:
        from bot import bot

        await bot.edit_message_text(
            chat_id=self.user.tgid,
            message_id=self.user.main_msg_id,
            text=self.text(**kwargs),
            reply_markup=self.markup,
        )
        return self.user.main_msg_id

    async def handle_callback(self, call: CallbackQuery) -> bool:
        return False

    async def handle_message(self, msg: Message):
        return False