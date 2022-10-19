import datetime

import requests
from CONSTANTS import (URL_BAN_LIST, URL_CHAT, URL_CLASS, URL_CURRENT_LESSONS,
                       URL_HOMEWORK, URL_PARAM, URL_SCHEDULE, URL_TIME_TABLE,
                       URL_USER, WEEKDAYS)
from tgbot.services.restapi.scripts import (return_error, send_error,
                                            send_success)
from tgbot.services.sub_classes import SheduleData


async def is_student(tguser_id):
    # есть ли в базе
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 200:
        return True
    if res.status_code == 404:
        return False
    return return_error(res)


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    # админ или нет
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 200:
        data = res.json()
        if data["data"]["is_admin"]:
            return True
        return False
    return return_error(res)


async def is_developer(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 404:
        return False
    elif res.status_code == 200:
        data = res.json()
        if data["data"]["is_superuser"]:
            return True
        return False
    return return_error(res)


async def register_user(tguser_id, classid, user_name):
    """Добавление юзера в бд к классу по ссылке, возвращает True если успешно"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER + URL_PARAM,
        json={
            "id": tguser_id,
            "platform": "tg",
            "class_token": classid,
            "name": user_name,
        },
    )
    if response.status_code == 201:
        return True
    if response.status_code == 404:
        await send_error(tguser_id, response, menu=False)
    if response.status_code == 403:
        await send_error(tguser_id, response, menu=False)
    return return_error(response)


async def register_class(tguser_id, data):
    """Добавление юзера в бд и создание класса, возвращает True если успешно"""
    # сначала регистрация полльзователя
    response = requests.post(
        URL_USER + URL_PARAM,
        json={"id": tguser_id, "platform": "tg", "name": data["user_name"]},
    )
    if response.status_code != 201:
        return return_error(response)

    # уже потом регистрация класса
    response = requests.post(
        URL_CLASS + URL_PARAM,
        json={
            "creator_platform": "tg",
            "creator_id": tguser_id,
            "name": f"Класс {data['user_name']}а",
        },
    )
    if response.status_code != 201:
        await delete_user(tguser_id, force=True)
        return return_error(response)

    # добавление звонков
    duration_lessons = {1: 55, 2: 60, 3: 65, 4: 60, 5: 55, 6: 55, 7: 60, 8: 60}
    start_time = data["start_time"]
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
            URL_TIME_TABLE + URL_PARAM,
            json={
                "creator_platform": "tg",
                "creator_id": tguser_id,
                "lesson_number": i,
                "begin_time": str(start_time),
                "end_time": str(end_time),
            },
        )
        d = d + datetime.timedelta(minutes=duration_lessons[i])
        if response.status_code != 201:
            await delete_user(tguser_id, force=True)
            return return_error(response)

    # расписание уроков
    schedule = data["shedule"].get_shedule()
    for el in schedule:
        day_n = schedule[el]["day_name"]
        for ell in schedule[el]["shedule"]:
            lesson_name = schedule[el]["shedule"][ell]
            if lesson_name != "":
                response = requests.post(
                    URL_SCHEDULE + URL_PARAM,
                    json={
                        "creator_platform": "tg",
                        "creator_id": tguser_id,
                        "day": day_n.lower(),
                        "lesson_number": ell + 1,
                        "lesson": lesson_name,
                    },
                )
                if response.status_code != 201:
                    await delete_user(tguser_id, force=True)
                    await send_error(tguser_id, response, menu=False)
                    return return_error(response)
    return True


async def delete_user(tguser_id, force=False):
    query = f"/tg/{tguser_id}"
    res = requests.delete(URL_USER + query + URL_PARAM + "&force=" + str(force))
    if res.status_code == 200:
        return True
    await send_error(tguser_id, res)
    return return_error(res)


async def ban_user(admin_tgid, user_tgid):
    pass


async def get_subjects_by_time(tguser_id):
    """По времени получает 2 ближайших предмета и возвращает список их названий"""
    query = f"/tg/{tguser_id}" + URL_PARAM
    res = requests.get(URL_CURRENT_LESSONS + query)
    if res.status_code == 200:
        data = res.json()["lessons"]
        return [_["lesson"]["name"] for _ in data]
    await send_error(tguser_id, res)
    return return_error(res)


async def is_lessons_in_saturday(tguser_id):
    """Делает запрос в БД и проверяет, есть ли уроки в субботу"""
    query = f"/tg/{tguser_id}/суббота"
    res = requests.get(URL_SCHEDULE + query + URL_PARAM)
    if res.status_code == 200:
        return True
    if (
        res.status_code == 404
        and res.json()["error"] == "Расписание на этот день не существует"
    ):
        return False
    return return_error(res)


async def add_homework(tguser_id, data, auto=False):
    """Добавляет домашку, если API вернуло ошибку - возвращает текст ошибки, иначе возвращает True"""
    payload = {
        "creator_platform": "tg",
        "creator_id": tguser_id,
        "lesson": data["subject"],
    }
    if auto:
        payload["date"] = "auto"
    else:
        payload["date"] = data["date"].strftime("%d-%m-%Y")
    if data["text"]:
        payload["text"] = data["text"]
    if data["files_tgid"]:
        payload["photos_tg_id"] = data["files_tgid"]

    response = requests.post(URL_HOMEWORK + URL_PARAM, json=payload)
    if response.status_code == 201:
        await send_success(tguser_id, response)
        return True
    await send_error(tguser_id, response)
    return return_error(response)


async def get_homework(userid, date, is_chat=False):
    """Возвращает домашку на дату"""
    if is_chat:
        userid *= -1  # HTTP не одобряет отрицательные числа (вернее знак "-")
    query = (
        f"/tg/{userid}/{date.strftime('%d-%m-%Y')}{URL_PARAM}&is_chat={str(is_chat)}"
    )
    res = requests.get(URL_HOMEWORK + query)
    if res.status_code == 200:
        lessons = res.json()["data"]
        hw = {}
        for data in lessons:
            lesson = data["schedule"]["lesson"]["name"]
            lesson_data = {
                "author": data["author_id"],
                "count": data["schedule"]["slot"]["number_of_lesson"],
                "text": data["text_homework"],
                "photos": [photo_id["photo_id"] for photo_id in data["photo_tg_id"]],
            }
            if lesson in hw:
                hw[lesson].append(lesson_data)
            else:
                hw[lesson] = [lesson_data]
        return [hw]
    if is_chat:
        userid *= -1
    await send_error(userid, res)
    return return_error(res)


async def get_schedule_on_date(tguser_id, date) -> list:
    query = f"/tg/{tguser_id}/{WEEKDAYS[date.weekday()]}"
    res = requests.get(URL_SCHEDULE + query + URL_PARAM)
    ret = []
    if res.status_code == 200:
        for lesson in res.json()["data"]:
            ret.append(lesson["lesson"]["name"])
    return ret


async def get_names_classmates(tguser_id):
    query = f"/students/tg/{tguser_id}"
    res = requests.get(URL_CLASS + query + URL_PARAM)
    if res.status_code == 200:
        students = res.json()["data"]
        students_names = {}
        for student in students:
            if student["tg_id"] != tguser_id:
                students_names[student["tg_id"]] = student["name"]
        return students_names
    await send_error(tguser_id, res)
    return return_error(res)


async def get_student_info(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 200:
        student = res.json()["data"]
        students_info = {
            "name": student["name"],
            "is_admin": student["is_admin"],
            "class_token": student["my_class"]["class_token"],
            "admins": student["class_admins"],
        }
        return students_info
    await send_error(tguser_id, res)
    return return_error(res)


async def change_class_token(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.patch(URL_CLASS + query + URL_PARAM, json={"class_token": "auto"})
    if res.status_code == 200:
        return True
    await send_error(tguser_id, res)
    return return_error(res)


async def assign_admin(tguser_id):
    query = f"/tg/{tguser_id}"
    res = requests.patch(URL_USER + query + URL_PARAM, json={"is_admin": True})
    if res.status_code == 200:
        return True
    await send_error(tguser_id, res)
    return return_error(res)


async def get_user_by_id(id):
    query = f"/no/{id}"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 200:
        return res.json()
    elif res.status_code == 404:
        return "Not found"
    return return_error(res)


async def get_all_users():
    query = "/all"
    res = requests.get(URL_USER + query + URL_PARAM)
    if res.status_code == 404:
        return return_error(res)
    return res.json()["data"]


async def register_chat(user_id, chat_id):
    params = {
        "user_tg_id": user_id,
        "chat_tg_id": chat_id,
    }
    res = requests.post(URL_CHAT + URL_PARAM, json=params)
    if res.status_code == 201:
        return True
    return return_error(res)


async def get_chat(chat_id):
    query = f"/tg/{chat_id}"
    res = requests.get(URL_CHAT + query + URL_PARAM)
    if res.status_code == 200:
        return res.json()["data"]
    return return_error(res)


async def is_registreted_chat(chat_id):
    query = f"/tg/{chat_id}"
    res = requests.get(URL_CHAT + query + URL_PARAM)
    if res.status_code == 200:
        return True
    elif res.status_code == 404:
        return False
    return return_error(res)


async def get_all_chats(tg_id):
    res = requests.get(URL_CHAT + f"/all/tg/{tg_id}" + URL_PARAM)
    if res.status_code == 200:
        return res.json()["data"]
    else:
        return return_error(res)


async def delete_chat(chat_id):
    res = requests.delete(URL_CHAT + f"/tg_tgchat/{chat_id}" + URL_PARAM)
    if res.status_code == 200:
        return True
    return return_error(res)


async def get_shedule(tguser_id):
    data = requests.get(URL_SCHEDULE + f"/tg/{tguser_id}" + URL_PARAM)
    if data.status_code == 200:
        res = SheduleData()
        res.load_shedule(data.json())
        return res
    return return_error(data)


async def ban_user(tguser_id, username):
    data = requests.post(
        URL_BAN_LIST + URL_PARAM, json={"user_tg_id": tguser_id, "username": username}
    )
    if data.status_code == 201:
        return True
    return return_error(data)


async def unban_user(id):
    data = requests.delete(URL_BAN_LIST + f"/{id}" + URL_PARAM)
    if data.status_code == 200:
        return True
    return return_error(data)


async def get_ban_list(tg_user_id):
    data = requests.get(URL_BAN_LIST + f"/class/tg/{tg_user_id}" + URL_PARAM)
    if data.status_code == 200:
        res = {}
        for i in data.json()["data"]:
            if tg_user_id != i["tg_id"]:
                res[i["username"]] = [i["id"]]
        return res
    return return_error(data)


async def get_study_days(tguser_id):
    data = requests.get(URL_SCHEDULE + f"/study_days/tg/{tguser_id}" + URL_PARAM)
    if data.status_code == 200:
        return data.json()["data"]
    return return_error(data)


# Получение списка рассылок
async def get_all_mailings() -> list:
    pass


# Отключение рассылки
async def turn_off_mailing():
    pass


# Включение рассылки
async def turn_on_mailing():
    pass


# Изменеие времени рассылки
async def change_mailing_time():
    pass
