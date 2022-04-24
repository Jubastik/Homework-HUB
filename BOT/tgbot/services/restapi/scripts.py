import logging

from BOT.bot import bot


# Скрипты Rest.
def return_error(response):
    logging.warning(f"Код ошибки: {response.status_code}. Ошибка: {response.json()['error']}")
    return {"code": response.status_code, "error": response.json()["error"]}


async def send_error(tguser_id, response):
    error_txt = f"Ошибка: {response.json()['error']}"
    await bot.send_message(tguser_id, error_txt)


async def send_success(tguser_id, response):
    await bot.send_message(tguser_id, response.json()['success'])
