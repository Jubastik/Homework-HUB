from aiogram.types import Message, CallbackQuery
from asyncio import sleep

from tgbot.entities.user import User

from service.restapi.api_error import ApiError
from service.restapi import restapi


class UsersManager:
    def __init__(self):
        self.users = {}  # {userid: User}
        # TODO: load users from database
        # 1) GET all users from database
        # 2) restore users without activating their stages
        # REDIS or MongoDB or DB???
        # data: userid, main_msg_id, mode, stage, other data (like start_time)

    async def get_user(self, userid: int) -> User:
        if userid in self.users:
            return self.users.get(userid)
        else:
            return await self._restore_user(userid)

    async def _restore_user(self, userid: int) -> User:
        # import here to avoid circular imports

        # try to restore user from database
        # if user is not in database, create new user
        # TODO: try to find main message id and his state

        user = User(self, userid)
        self.users[userid] = user
        return user

    def restore_from_database(self, userid: int) -> User | None:
        return None

    async def handle_message(self, msg: Message) -> None:
        userid = msg.from_user.id
        user = await self.get_user(userid)
        handled = await user.handle_message(msg)
        if not handled:
            await msg.delete()
            if user.main_msg_id:
                warning = await msg.answer("Используй кнопки 👆🏻")
                await sleep(3)
                await warning.delete()
            else:
                warning = await msg.answer("Используй команду /start")
                await sleep(15)
                await warning.delete()

    async def handle_callback(self, call: CallbackQuery) -> None:
        userid = call.from_user.id
        user = await self.get_user(userid)
        # If user has old message, delete it
        if call.message.message_id != user.main_msg_id:
            await call.answer("Устаревший запрос, попробуй снова")
            await call.message.delete()
            return
        handled = await user.handle_callback(call)
        if not handled:
            pass
