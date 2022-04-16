# Функции запросов на rest api (использовать await!)
# Пока что просто затычки => фильтры работают через жопу, надо в коде указывать кем воспринимать юзеров
import json
import requests
import random
from CONSTANTS import URL_USER, URL_CLASS


# Tasks:
# !1) Реализация используемых фильтрами is_student, is_admin, is_developer
# 2) add_user


async def is_student(tguser_id):
    # есть ли в базе
    query = f"/tg/{tguser_id}"
    if requests.get(URL_USER + query):
        res = requests.get(URL_USER + query)
        res = json.loads(res.text)
        return True
    return False


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    # админ или нет
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    res = json.loads(res.text)
    if res['is_admin']:
        return True
    else:
        return False


async def is_developer(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query)
    res = json.loads(res.text)
    if res['is_superuser']:
        return True
    else:
        return False


# Вообще по хорошему создать вспомогательный класс для homework, так будет удобней и красивше.
async def add_homework(tguser_id, homework: dict):
    pass


def register_user(tguser_id, classid):
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
    if response:
        return True
    else:
        return False


def register_class(tguser_id, data):
    """Добавление юзера в бд и создание класса, возвращает True если успешно, в противном случае False"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER, json={"id": tguser_id, "platform": "tg", "name": "Олег"}
    )
    print(response)
    if not response:
        return False
    # уже потом регистрация класса
    response = requests.post(
        URL_CLASS,
        json={"creator_platform": "tg", "creator_id": tguser_id, "name": "10A"},
    )
    if not response:
        return False

    return True
