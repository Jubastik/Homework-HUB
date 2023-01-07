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

import aiohttp


async def get_student():
    async with aiohttp.ClientSession() as session:
        async with session.get(
            "http://localhost:8000/students/?root_token=no_token&obj_id=1&id_type=student_tg"
        ) as response:
            return await response.json()
