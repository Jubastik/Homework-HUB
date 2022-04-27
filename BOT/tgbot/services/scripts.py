from unicodedata import name
from BOT.tgbot.services.restapi.restapi import is_lessons_in_saturday, get_homework
import datetime
from BOT.CONSTANTS import WEEKDAYS


def time_is_correct(time: list):
    try:
        hours, minutes = map(int, time.split(":"))
        if hours < 0 or minutes < 0 or hours > 24 or minutes > 60:
            return False
        if hours != hours or minutes != minutes:
            return False
        return [str(hours), str(minutes)]
    except:
        return False


def convert_time(time: list):
    if len(time[1]) == 1:
        time[1] = f"1{time[1]}"
    return time


def convert_position(pos):
    return [((pos) // 8), (pos % 8)]


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


def convert_homework(data) -> dict:
    res = []
    for lesson, lesson_data in data.items():
        # Какой-то алгоритм выбора домашки, которого нету ._.
        lesson_data = lesson_data[0]
        # Формирование текста и фото
        txt = lesson_data["text"] if lesson_data["text"] is not None else ""
        info = {
            "text": "\n".join([f"{lesson}:", txt]),
            "photos": lesson_data["photos"],
        }
        res.append(info)
    return res


def convert_user_info(data) -> str:
    res = "\n".join(
        [
            "Профиль:",
            f"Имя: @{data['name']}",
            "Админ: ✅" if data["is_admin"] else "Админ: ❌",
            f"Токен класса: {data['class_token']}",
            f"Админы класса: {' '.join(['@' + i for i in data['admins']])}",
        ]
    )
    return res
