# TODO:

# CHECKERS:
# is_student ✅
# is_admin ✅
# is_developer ✅
# is_lessons_in_saturday ✅
# get_user_by_db_id
# get_user ✅

# Register:
# register_user ✅
# register_class ✅
# ban_user

# UPDATE:
# change_class_token ✅
# assign_admin
#

# POST:
# !add_homework ✅


# GET:
# get_class ✅
# get_subjects_by_time
# get_homework ✅
# get_schedule_on_date ✅
# get_names_classmates
# get_student_info ✅
# get_all_users
# get_shedule ✅
# get_ban_list
# get_study_days ✅
#

# DELETE:
# delete_user
# unban_user


import datetime

from CONSTANTS import WEEKDAYS
from services.restapi.api_error import ApiError
from services.restapi.formatters import f_days_from_schedules, create_time_tables
from services.restapi.session import aiohttp_session, add_tg_id

from services.restapi.URLS import URL_STUDENT, URL_CLASS, URL_SCHEDULE, URL_HOMEWORK


async def _get_user(session, params, tg_id: int):
    params = add_tg_id(params)
    async with session.get(URL_STUDENT + str(tg_id), params=params) as response:
        status = response.status
        return status, await response.json()


@aiohttp_session
async def get_user(session, params, tg_id: int):
    status, json = await _get_user(session, params, tg_id)
    if status == 200:
        return json
    else:
        return ApiError(status, json)


@aiohttp_session
async def is_student(session, params, tg_id: int):
    status, json = await _get_user(session, params, tg_id)
    if status == 200:
        return True
    elif status == 404:
        return False
    else:
        return ApiError(status, json)


@aiohttp_session
async def is_admin(session, params, tg_id: int):
    status, json = await _get_user(session, params, tg_id)
    if status == 200:
        return json["is_admin"] is True
    else:
        return ApiError(status, json)


@aiohttp_session
async def is_superuser(session, params, tg_id: int):
    status, json = await _get_user(session, params, tg_id)
    if status == 200:
        return json["is_superuser"] is True
    else:
        return ApiError(status, json)


@aiohttp_session
async def create_user(session, params, tg_id: int, name: str, class_token: int = None):
    json = {"tg_id": tg_id, "name": name}
    if class_token is not None:
        json["class_token"] = class_token
    async with session.post(URL_STUDENT, params=params, json=json) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def create_class(session, params, tg_id: int, class_name: str, start_time: datetime.time, schedules):
    # Пример: schedules = [{"lesson": "string", "day_of_week": "понедельник", "lesson_number": 1}]
    time_tables = create_time_tables(start_time)

    params = add_tg_id(params, tg_id)
    json = {
        "name": class_name,
        "schedules": schedules,
        "time_tables": time_tables,
    }
    async with session.post(URL_CLASS, params=params, json=json) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def change_class_token(session, params, tg_id: int, class_token="auto"):
    params = add_tg_id(params)
    json = {"class_token": class_token}
    async with session.patch(URL_CLASS + str(tg_id), params=params, json=json) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def get_class(session, params, tg_id: int):
    params = add_tg_id(params)
    async with session.get(URL_CLASS + str(tg_id), params=params) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


async def _get_schedule(session, params, tg_id: int, date: datetime.date = None):
    # TODO: сейчас во время воскресенья возвращается ошибка, если нужно, можно возвращать пустой список
    day_of_week = ""
    if date is not None:
        day_of_week = WEEKDAYS[date.weekday()]
    params = add_tg_id(params, tg_id)
    async with session.get(URL_SCHEDULE + day_of_week, params=params) as response:
        status = response.status
        return status, await response.json()


@aiohttp_session
async def get_schedule(session, params, tg_id: int, date: datetime.date = None):
    status, json = await _get_schedule(session, params, tg_id, date)
    if status == 200:
        return json
    else:
        return ApiError(status, json)


@aiohttp_session
async def get_study_week_days(session, params, tg_id: int):
    status, json = await _get_schedule(session, params, tg_id)
    if status == 200:
        return f_days_from_schedules(json)
    else:
        return ApiError(status, json)


@aiohttp_session
async def is_lessons_in_saturday(session, params, tg_id: int):
    status, json = await _get_schedule(session, params, tg_id)
    if status == 200:
        return "суббота" in f_days_from_schedules(json)
    else:
        return ApiError(status, json)


@aiohttp_session
async def get_current_lessons(session, params, tg_id: int):
    params = add_tg_id(params)
    async with session.get(URL_SCHEDULE + "current_schedule/" + str(tg_id), params=params) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def get_next_lesson_date(session, params, tg_id: int, lessons: list[str]):
    params = add_tg_id(params)
    params["lessons"] = lessons
    async with session.get(URL_SCHEDULE + "next_date/" + str(tg_id), params=params) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def create_homework(
    session,
    params,
    tg_id: int,
    lesson: str,
    date: datetime.date,
    text_homework: str = None,
    photo_tg_ids: list[int] = None,
):
    params = add_tg_id(params, tg_id)
    json = {"author_tg_id": tg_id, "lesson": lesson, "date": str(date)}
    if text_homework is not None:
        json["text_homework"] = text_homework
    if photo_tg_ids is not None:
        json["photo_tg_id"] = photo_tg_ids
    async with session.post(URL_HOMEWORK, params=params, json=json) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def get_homework(session, params, tg_id: int, date: datetime.date):
    params = add_tg_id(params, tg_id)
    async with session.get(URL_HOMEWORK + str(date), params=params) as response:
        status = response.status
        if status == 200:
            return await response.json()
        else:
            return ApiError(status, await response.json())
