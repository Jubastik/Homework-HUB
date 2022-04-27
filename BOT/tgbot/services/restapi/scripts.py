import logging

from BOT.bot import bot
from BOT.tgbot.keyboards.inline.markup import markup_menu
from BOT.tgbot.services.sub_classes import RestErorr


# Скрипты Rest.
def return_error(response):
    err = RestErorr(response)
    logging.warning(f"Код ошибки: {err.status_code}. Ошибка: {err.error_message}")
    return err


async def send_error(tguser_id, response, menu=True):
    error_txt = f"Ошибка: {response.json()['error']} /start"
    if menu:
        await bot.send_message(tguser_id, error_txt, reply_markup=markup_menu)
    else:
        await bot.send_message(tguser_id, error_txt)


async def send_success(tguser_id, response):
    await bot.send_message(tguser_id, response.json()["success"])
