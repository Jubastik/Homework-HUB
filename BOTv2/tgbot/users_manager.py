from aiogram.types import Message, CallbackQuery

from tgbot.entities.user import User


class UsersManager:
    def __init__(self):
        self.users = {}  # {userid: User}

    async def get_user(self, userid: int) -> User:
        if userid in self.users:
            return self.users.get(userid)
        else:
            return await self._restore_user(userid)

    async def _restore_user(self, userid: int) -> User:
        # import here to avoid circular imports
        from tgbot.modes.registration.registration_mode import RegistrationMode

        # try to restore user from database
        # if user is not in database, create new user
        # TODO: try to find main message id and his state
        user = User(self, userid)
        mode = RegistrationMode(user)
        await user.init(mode)  # if can find main message, pass it to mode.init()
        self.users[userid] = user
        return user

    async def handle_message(self, msg: Message) -> None:
        userid = msg.from_user.id
        user = await self.get_user(userid)
        handled = await user.handle_message(msg)
        if not handled:
            pass

    async def handle_callback(self, call: CallbackQuery) -> None:
        userid = call.from_user.id
        user = await self.get_user(userid)
        handled = await user.handle_callback(call)
        if not handled:
            pass

    def handle_api_error(self, error) -> None:
        pass
