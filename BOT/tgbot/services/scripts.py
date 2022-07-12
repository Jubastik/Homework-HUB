import datetime

from tgbot.services.restapi.restapi import get_user_by_id
from CONSTANTS import WEEKDAYS
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text


def time_is_correct(time: list):
    try:
        hours, minutes = map(int, time.split(":"))
        if hours < 0 or minutes < 0 or hours > 24 or minutes > 60:
            return False
        return [str(hours), str(minutes)]
    except:
        return False


def convert_time(time: list):
    if len(time[1]) == 1:
        time[1] = f"0{time[1]}"
    return time


def generate_dates(saturday_lesson) -> list:
    """Генерирует даты"""
    dates = []
    if isinstance(saturday_lesson, dict):
        return saturday_lesson
    # Вот так вот если is_lessons_in_saturday() возвращает True для 19.04
    today = datetime.date.today()
    c = 1
    while c <= 7:
        # дата числом
        day = today + datetime.timedelta(days=c)
        # день недели
        day_name = datetime.datetime.weekday(day)
        # воскресенье пропускаем
        if saturday_lesson:
            if day_name == 6:
                pass
            else:
                dates.append([f'{day.strftime("%d.%m")} {WEEKDAYS[day_name]}', day])
        else:
            if day_name == 6 or day_name == 5:
                pass
            else:
                dates.append([f'{day.strftime("%d.%m")} {WEEKDAYS[day_name]}', day])
        c += 1
    return dates


async def convert_homework(data, callback) -> dict:
    res = []
    for lesson, lesson_data in data.items():
        for data in lesson_data:
            # Формирование текста и фото
            txt = data["text"] if data["text"] is not None else ""
            author_data = await get_user_by_id(data["author"])
            author_name = author_data["data"]["name"]
            info = {
                "text": process_text(TextKeys.homework_txt, callback, subject=lesson, author=author_name, txt=txt),
                "photos": data["photos"],
            }
            res.append(info)
    return res

    # {предмет: [{txt: txt, photo: [photos]}]}


def convert_users(data):
    txt = "\n".join(
        [
            "Панель управления классом⭐️",
            "Список одноклассников:",
            *["@" + data[i] for i in data.keys()],
        ]
    )
    return txt
