from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageToDeleteNotFound
import logging
from asyncio import sleep

from tgbot.entities.user import User

from services.restapi.api_error import ApiError
from services.restapi import restapi


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
            try:
                await msg.delete()
            except MessageCantBeDeleted as err:
                logging.warning(
                    f"UM.handle_message:Can't delete message from {userid} - {msg.from_user.username or msg.from_user.first_name + ' ' + msg.from_user.last_name}"
                    + str(err)
                )
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
            await call.answer("Устаревший запрос, напиши /start", show_alert=True)
            try:
                await call.message.delete()
            except (AttributeError, MessageCantBeDeleted, MessageToDeleteNotFound) as err:
                # Удаляет None значения
                names = filter(
                    lambda x: x, [call.from_user.username, call.from_user.first_name, call.from_user.last_name]
                )
                name = " ".join(names)
                logging.warning(f"UM.handle_callback:Can't delete message from {userid} - {name}" + str(err))
            return
        handled = await user.handle_callback(call)
        if not handled:
            from bot import bot

            await call.answer()
            await bot.send_message(f"Callback is't handled DATA:\n call_data: {call.data}")
            await logging.critical(
                f"Callback is't handled DATA:\n call_data: {call.data}\n userid: {userid}\n cur_stage: {user.mode.current_stage}"
            )
