import aiohttp

from CONSTANTS import API_TOKEN


def aiohttp_session(func):
    async def wrapper(*args, **kwargs):
        async with aiohttp.ClientSession() as session:
            params = {
                "root_token": API_TOKEN,
            }
            await func(session, params, *args, **kwargs)

    return wrapper
