from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.handlers.registration.stages.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_join_by_id_stage,
    get_markup_student_menu,
)
from tgbot.FSM.states import StudentMenu
from tgbot.services.restapi.restapi import (
    is_admin,
    register_user,
)
from tgbot.services.scripts import make_username
from tgbot.services.sub_classes import RestErorr

from bot import bot


class JoinByIdStage(Stage):
    def __init__(self, rm) -> None:
        self.rm = rm
        self.markup = markup_join_by_id_stage

    async def activate(self, call: CallbackQuery = None, status=""):
        await bot.edit_message_text(
            chat_id=self.rm.userid,
            message_id=self.rm.main_message_id,
            text=process_text(TextKeys.get_class_token, call, status=status),
            reply_markup=self.markup,
        )
        await call.answer()

    async def on_message(self, msg: Message):
        classid = msg.text
        if classid.isdigit():
            username = make_username(User.get_current())
            res = await register_user(self.rm.userid, classid, username)
            if isinstance(res, RestErorr):
                await self.activate(status="something went wrong, try again")
                await sleep(1)
                await msg.delete()
                return
            print("await self.rm.registred()")
            # await self.rm.registred()
            await self.rm.FSMContext.reset_state()
            await StudentMenu.Menu.set()
            res = await is_admin(msg.from_user.id)
            if isinstance(res, RestErorr):
                return
            await msg.answer(
                process_text(TextKeys.menu, msg),
                reply_markup=get_markup_student_menu(res),
            )
        else:
            await self.activate(status=process_text(TextKeys.wrong_class_token, msg))
            await sleep(1)
            await msg.delete()