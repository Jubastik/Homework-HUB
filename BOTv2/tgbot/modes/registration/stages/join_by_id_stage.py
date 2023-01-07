from aiogram.types import CallbackQuery, Message, User
from asyncio import sleep

from tgbot.entities.stage import Stage
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text
from tgbot.keyboards.inline.markup import (
    markup_join_by_id_stage,
    get_markup_student_menu,
)
from services.restapi.restapi import (
    is_admin,
    register_user,
)
from services.scripts import make_username
from services.sub_classes import RestErorr

from bot import bot


class JoinByIdStage(Stage):
    name = "join_by_id_stage"

    def __init__(self, mode) -> None:
        super().__init__(mode)
        self.markup = markup_join_by_id_stage

    async def activate(self, status="") -> int:
        await bot.edit_message_text(
            chat_id=self.user.tgid,
            message_id=self.user.main_msg_id,
            text=process_text(TextKeys.get_class_token, status=status),
            reply_markup=self.markup,
        )
        return self.user.main_msg_id

    async def handle_message(self, msg: Message) -> bool:
        classid = msg.text
        if classid.isdigit():
            username = make_username(User.get_current())
            print(f"await register_user({self.user.tgid}, {classid}, {username})")
            # res = await register_user(self.rm.userid, classid, username)
            # if isinstance(res, RestErorr):
            #     await self.activate(status="something went wrong, try again")
            #     await sleep(1)
            #     await msg.delete()
            #     return True
            # print("await self.rm.registred()")
            # # await self.rm.registred()
            # res = await is_admin(msg.from_user.id)
            # if isinstance(res, RestErorr):
            #     return True
            # await msg.answer(
            #     process_text(TextKeys.menu, msg),
            #     reply_markup=get_markup_student_menu(res),
            # )
            # return True
        else:
            await self.activate(status=process_text(TextKeys.wrong_class_token, msg))
            await sleep(1)
        await msg.delete()
        return True