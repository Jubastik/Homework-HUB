# Функции запросов на rest api (использовать await!)
# Пока что просто затычки => фильтры работают через жопу, надо в коде указывать кем воспринимать юзеров
import json
import time

import requests
import random
import datetime
from BOT.CONSTANTS import URL_USER, URL_CLASS, URL_SCHEDULE, URL_HOMEWORK, URL_TIME_TABLE, URL_CURRENT_LESSONS
from BOT.tgbot.services.restapi.scripts import return_error
from BOT.tgbot.services.sub_classes import SheduleData


# Tasks:
# !1) Реализация используемых фильтрами is_student, is_admin, is_developer
# 2) add_user


async def is_student(tguser_id):
    # есть ли в базе
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    if res.status_code == 200:
        return True
    return False


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    # админ или нет
    # query = f"/tg/{tguser_id}"
    # res = requests.get(URL_USER + query)
    # res = json.loads(res.text)
    # if res["data"]['is_admin']:
    #     return True
    # else:
    #     return False
    return True


async def is_developer(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    res = json.loads(res.text)
    if res["data"]["is_superuser"]:
        return True
    else:
        return False


async def register_user(tguser_id, classid, user_name):
    """Добавление юзера в бд к классу по ссылке, возвращает True если успешно, в противном случае False"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER,
        json={
            "id": tguser_id,
            "platform": "tg",
            "class_token": classid,
            "name": user_name,
        })
    if response.status_code == 200:
        return True
    return False


async def register_class(tguser_id, data):
    """Добавление юзера в бд и создание класса, возвращает True если успешно, в противном случае False"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER, json={"id": tguser_id, "platform": "tg", "name": data['user_name']}
    )
    if response.status_code != 200:
        return False
    # уже потом регистрация класса
    response = requests.post(
        URL_CLASS,
        json={"creator_platform": "tg", "creator_id": tguser_id, "name": "10A"}
    )
    # добавление звонков
    duration_lessons = {1: 55, 2: 60, 3: 65, 4: 60, 5: 55, 6: 55, 7: 60, 8: 60}
    start_time = data['start_time']
    date_now = datetime.date.today()
    start = datetime.time(int(start_time[0]), int(start_time[1]))
    my_datetime = datetime.datetime.combine(date_now, start)
    d = my_datetime
    for i in range(1, 9):
        a = (d + datetime.timedelta(minutes=1)).time()
        start_time = a.strftime("%H:%M")
        b = (d + datetime.timedelta(minutes=duration_lessons[i])).time()
        end_time = b.strftime("%H:%M")
        response = requests.post(
            URL_TIME_TABLE, json={"creator_platform": "tg",
                                  "creator_id": tguser_id,
                                  "lesson_number": i,
                                  "begin_time": str(start_time),
                                  "end_time": str(end_time)}
        )
        d = d + datetime.timedelta(minutes=duration_lessons[i])

    # расписание уроков
    schedule = data['shedule'].get_shedule()
    for el in schedule:
        day_n = schedule[el]['day_name']
        for ell in schedule[el]['shedule']:
            if schedule[el]['shedule'][ell] != '-':
                response = requests.post(
                    URL_SCHEDULE,
                    json={"creator_platform": "tg",
                          "creator_id": tguser_id,
                          "day": day_n.lower(),
                          "lesson_number": ell + 1,
                          "lesson": schedule[el]['shedule'][ell]}
                )
    return True


async def delete_user(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.delete(URL_USER + query)
    res = json.loads(res.text)
    if res.status_code == 200:
        return True
    return res['error']


async def get_subjects_by_time(tguser_id, date_time=datetime.datetime.now()) -> list():
    """По времени получает 2 ближайших предмета"""
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_CURRENT_LESSONS)
    res = json.loads(res.text)
    return [res[-2]['lesson_name'], res[-1]['lesson_name']]


async def is_lessons_in_saturday(tguser_id):
    """Делает запрос в БД и проверяет, есть ли уроки в субботу"""
    query = f"/tg/{tguser_id}/суббота"
    res = requests.get(URL_SCHEDULE + query)
    if res.status_code == 200:
        return True
    else:
        return False


async def add_homework(tguser_id, data, auto=False):
    """Добавляет домашку, если API вернуло ошибку - возвращает текст ошибки, иначе возвращает True"""
    response = requests.post(
        URL_HOMEWORK,
        json={"creator_platform": "tg",
              "creator_id": tguser_id,
              "date": datetime.date.today(),
              "lesson": data['subject'],
              "text": data['text']}
    )
    if response.status_code == 200:
        return True
    return return_error(response)


async def get_homework(tguser_id, date):
    """Возвращает домашку на дату (дата в формате 25-04-2022)"""
    query = f"/tg/{tguser_id}/{date}"
    res = requests.get(URL_HOMEWORK + query)
    if res.status_code == 200:
        a = json.loads(res.text)
        hw = {}
        for el in a:
            hw['lesson'] = el['lesson']
            hw['text'] = el['text']
        return hw
    return False


# def get_all_homework(tguser_id):
#     query = f"/tg/{tguser_id}"
#     res = requests.get(URL_HOMEWORK + query)
#     if res.status_code == 200:
#         a = json.loads(res.text)
#         hw = {}
#         for el in a:
#             hw['date'] = el['date']
#             hw['lesson'] = el['lesson']
#             hw['text'] = el['text']
#         return hw
#     return False


async def get_schedule_on_date(tguser_id, date) -> list:
    return [
        "Русский🇷🇺",
        "Литература📚",
        "Алгебра🔢",
        "Геометрия📐",
        "Биология🌿",
        "География🌐",
    ]  # Затычка


def get_all_users(tguser_id):
    pass
