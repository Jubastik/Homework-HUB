# TODO:

# CHECKERS:
# is_student
# is_admin
# is_developer
# is_lessons_in_saturday
# get_user_by_id

# Register:
# register_user
# register_class
# ban_user

# UPDATE:
# change_class_token
# assign_admin
#

# POST:
# add_homework


# GET:
# get_class
# get_subjects_by_time
# get_homework
# get_schedule_on_date
# get_names_classmates
# get_student_info
# get_all_users
# get_shedule
# get_ban_list
# get_study_days
#

# DELETE:
# delete_user
# unban_user

# Пример асинхронного запроса к API
from services.restapi.api_error import ApiError
from services.restapi.session import aiohttp_session, add_tg_id

from services.restapi.URLS import URL_STUDENT


@aiohttp_session
async def test(session, params):
    async with session.get(URL_STUDENT, params=params) as response:
        status = response.status
        if status == 200:
            json = await response.json()
            print(json)
            return json
        else:
            json = await response.text()
            print(json)
            return json


@aiohttp_session
async def get_user(session, params, tg_id):
    params = add_tg_id(params, tg_id)
    async with session.get(URL_STUDENT, params=params) as response:
        status = response.status
        if status == 200:
            json = response.json()
            return json
        else:
            return ApiError(status, await response.json())


@aiohttp_session
async def is_student(session, params, tg_id):
    params = add_tg_id(params, tg_id)
    async with session.get(URL_STUDENT + tg_id, params=params) as response:
        status = response.status
        if status == 200:
            return True
        elif status == 404:
            return False
        else:
            return ApiError(status, await response.json())
