import logging

from bot import bot
from tgbot.keyboards.inline.markup import markup_menu, markup_error_menu
from tgbot.services.sub_classes import RestErorr


# Скрипты Rest.
def return_error(response):
    err = RestErorr(response)
    logging.warning(f"Код ошибки: {err.status_code}. Ошибка: {err.error_message}")
    return err


async def send_error(tguser_id, response, menu=True):
    error_txt = f"Ошибка: <i>{response.json()['error']}</i>"
    if menu:
        await bot.send_message(tguser_id, error_txt, reply_markup=markup_error_menu)
    else:
        await bot.send_message(tguser_id, error_txt)


async def send_success(tguser_id, response):
    await bot.send_message(tguser_id, response.json()["success"])
