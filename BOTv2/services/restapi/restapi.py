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
from services.restapi.session import aiohttp_session


@aiohttp_session
async def test(session, params):
    async with session.get(f"http://localhost:8000/students/", params=params) as response:
        status = response.status
        if status == 200:
            json = await response.json()
            print(json)
            return json
        else:
            json = await response.text()
            print(json)