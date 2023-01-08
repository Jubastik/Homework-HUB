import aiohttp

from CONSTANTS import API_TOKEN


def aiohttp_session(func):
    async def wrapper(*args, **kwargs):
        headers = {"X-Requested-With": "XMLHttpRequest", "Content-Type": "application/json"}
        async with aiohttp.ClientSession(headers=headers) as session:
            params = {
                "root_token": API_TOKEN,
            }
            res = await func(session, params, *args, **kwargs)
            return res

    return wrapper


def add_tg_id(params, tg_id):
    params["id_type"] = "student_tg"
    params["obj_id"] = tg_id
    return params
