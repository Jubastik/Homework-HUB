from aiogram import types


class Handlers:
    def __init__(self, bot, dp):
        self.bot = bot
        self.dp = dp

    def register_handlers(self):
        self.dp.register_message_handler(self.hello_world, commands=["start"])

    async def hello_world(self, message: types.Message):
        await message.reply("Hello world", reply=False)
