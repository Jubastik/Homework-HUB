from aiogram.types import CallbackQuery, Message

from services.restapi.api_error import ApiError


class Stage:  # Abstract class
    name = "entry_stage"

    def __init__(self, mode):
        self.mode = mode
        self.user = mode.user
        self.text: function = lambda *args, **kwargs: "No activate method"
        self.markup: function = lambda *args, **kwargs: None

    async def get_args(self) -> dict:
        return {"markup_args": {}, "text_args": {}}

    def merge_args(self, args1, args2) -> dict:
        return {**args1, **args2}

    async def _prepare_args(self, markup_args={}, text_args={}, **kwargs):
        args = await self.get_args()
        if isinstance(args, ApiError):
            return args
        markup_args = self.merge_args(args["markup_args"], markup_args)
        text_args = self.merge_args(args["text_args"], text_args)
        return {"markup_args": markup_args, "text_args": text_args}

    async def activate(self, markup_args={}, text_args={}, **kwargs) -> int:
        msg_args = await self._prepare_args(markup_args, text_args, **kwargs)

        from bot import bot

        msg = await bot.edit_message_text(
            chat_id=self.user.tgid,
            message_id=self.user.main_msg_id,
            text=self.text(**msg_args["text_args"]),
            reply_markup=self.markup(**msg_args["markup_args"]),
            **kwargs,
        )
        return msg.message_id

    async def new_message(self, markup_args={}, text_args={}, **kwargs) -> int:
        msg_args = await self._prepare_args(markup_args, text_args, **kwargs)

        from bot import bot

        msg = await bot.send_message(
            chat_id=self.user.tgid,
            text=self.text(**msg_args["text_args"]),
            reply_markup=self.markup(**msg_args["markup_args"]),
            **kwargs,
        )
        return msg.message_id

    async def handle_callback(self, call: CallbackQuery) -> bool:
        return False

    async def handle_message(self, msg: Message):
        return False

    async def handle_api_error(self, error) -> bool:
        handled = await self.mode.handle_api_error(error)
        if handled:
            return True
        return False
