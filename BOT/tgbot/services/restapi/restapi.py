# Функции запросов на rest api (использовать await!)
# Пока что просто затычки => фильтры работают через жопу, надо в коде указывать кем воспринимать юзеров
import json
import requests
import random
import datetime
from BOT.CONSTANTS import URL_USER, URL_CLASS, URL_SCHEDULE, URL_HOMEWORK
from BOT.tgbot.services.sub_classes import SheduleData


# Tasks:
# !1) Реализация используемых фильтрами is_student, is_admin, is_developer
# 2) add_user


async def is_student(tguser_id):
    # есть ли в базе
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    if res.status_code == 404:
        return False
    res = json.loads(res.text)
    return True


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    # админ или нет
    # query = f"/tg/{tguser_id}"
    # res = requests.get(URL_USER + query)
    # res = json.loads(res.text)
    # if res["is_admin"]:
    #     return True
    # else:
    #     return False
    return True


async def is_developer(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    res = json.loads(res.text)
    if res["is_superuser"]:
        return True
    else:
        return False


async def register_user(tguser_id, classid, username):
    """Добавление юзера в бд к классу по ссылке, возвращает True если успешно, в противном случае False"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER,
        json={
            "id": tguser_id,
            "platform": "tg",
            "class_token": classid,
            "name": "Олег",
        },
    )
    if response.status_code == 200:
        return True
    return False


async def register_class(tguser_id, data):
    """Добавление юзера в бд и создание класса, возвращает True если успешно, в противном случае False"""
    # сначала регистрация полльзователя
    # response = requests.post(
    #     URL_USER, json={"id": tguser_id, "platform": "tg", "name": "Олег"}
    # )
    # if response.status_code == 404:
    #     return False
    # # уже потом регистрация класса
    # response = requests.post(
    #     URL_CLASS,
    #     json={"creator_platform": "tg", "creator_id": tguser_id, "name": "10A"}
    # )
    # schedule = data['shedule'].SheduleData.get_shedule()
    # for el in schedule:
    #     day_n = schedule[el]['day_name']
    #     for ell in schedule[el]['shedule']:
    #         response = requests.post(
    #             URL_SCHEDULE,
    #             json={"creator_platform": "tg",
    #                   "creator_id": tguser_id,
    #                   "day": day_n,
    #                   "lesson_number": ell,
    #                   "lesson": schedule[el]['shedule'][ell]}
    #         )
    # return True
    return True


async def delete_user(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.delete(URL_USER + query)
    if res.status_code == 200:
        return True
    return False


async def get_subjects_by_time(tguser_id, date_time=datetime.datetime.now()) -> list():
    """По времени получает 2 ближайших предмета"""
    return ["Русский🇷🇺", "Литература📚"]  # Затычка


async def is_lessons_in_saturday(tguser_id):
    """Делает запрос в БД и проверяет, есть ли уроки в субботу"""
    query = f"/tg/{tguser_id}/сб"
    res = requests.get(URL_SCHEDULE + query)
    if res.status_code == 200:
        return True
    else:
        return False


async def add_homework(tguser_id, data, auto=False):
    """Добавляет домашку, если API вернуло ошибку - возвращает текст ошибки, иначе возвращает True"""
    response = requests.post(
        URL_HOMEWORK,
        json={
            "creator_platform": "tg",
            "creator_id": tguser_id,
            "date": "26-04-2022",
            "lesson": "Русс",
            "text": "№5",
        },
    )
    if response.status_code == 200:
        return True
    return False


async def get_homework(tguser_id):
    """Возвращает домашку на сегодня"""
    query = f"/tg/{tguser_id}/{datetime.date.today()}"
    res = requests.get(URL_HOMEWORK + query)
    if res.status_code == 200:
        return json.loads(res.text)
    return False


async def get_schedule_on_date(tguser_id, date) -> list:
    return [
        "Русский🇷🇺",
        "Литература📚",
        "Алгебра🔢",
        "Геометрия📐",
        "Биология🌿",
        "География🌐",
    ]  # Затычка
