from bot import TgBot
from config import TOKEN


def launch():
    bot = TgBot(TOKEN)
    bot.start()


if __name__ == '__main__':
    launch()