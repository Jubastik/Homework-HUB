from CONSTANTS import API_TOKEN


def aiohttp_session(func):
    async def wrapper(*args, **kwargs):
        from bot import session

        params = {
            "root_token": API_TOKEN,
        }
        res = await func(session, params, *args, **kwargs)
        return res

    return wrapper


def add_tg_id(params, tg_id: int = None):
    params["id_type"] = "student_tg"
    if tg_id is not None:
        params["obj_id"] = tg_id
    return params
