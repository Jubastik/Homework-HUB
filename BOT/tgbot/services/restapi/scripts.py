from BOT.bot import bot


# Скрипты Rest.
def return_error(response):
    return {"code": response.status_code, "error": response.json()["error"]}


async def send_error(tguser_id, error_txt):
    await bot.send_message(tguser_id, error_txt)
