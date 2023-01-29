import datetime
from asyncio import sleep

from CONSTANTS import WEEKDAYS, WEEKDAYS_TRASNLATE
from languages.text_keys import TextKeys
from languages.text_proccesor import process_text

# from service.restapi.restapi import get_user_by_id


def time_is_correct(time: list):
    try:
        hours, minutes = map(int, time.split(":"))
        if hours < 0 or minutes < 0 or hours > 24 or minutes > 60:
            return False
        return [str(hours), str(minutes)]
    except:
        return False


def convert_time(time: list):
    time = time.split(":")
    hours, minutes = map(int, time)
    return datetime.time(hours, minutes)


def generate_dates(saturday_lesson) -> list:
    """Генерирует даты"""
    dates = []
    if isinstance(saturday_lesson, dict):
        return saturday_lesson
    # Вот так вот если is_lessons_in_saturday() возвращает True для 19.04
    today = datetime.date.today()
    c = 0
    while c <= 6:
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


def generate_dates_back(weekdays) -> list:
    """Генерирует даты за последние 14 дней"""
    # weekdays = weekdays_to_num(weekdays)
    now = datetime.datetime.now()
    dates = []
    for i in range(21):
        day = now - datetime.timedelta(days=i)
        day_name = day.weekday()
        if WEEKDAYS[day_name] in weekdays:
            dates += [[f'{day.strftime("%d.%m")}, {WEEKDAYS[day_name]}', day.date()]]
    return dates


def convert_homework(data, callback, diary_data=None) -> dict:
    res = []
    data.sort(key=lambda x: x["schedule"]["slot"]["number_of_lesson"])
    for homework in data:
        # Формирование текста и фото
        txt = homework["text_homework"] if homework["text_homework"] is not None else ""
        author_name = homework["author"]["name"]
        subject = homework["schedule"]["lesson"]["name"]
        hw = {
            "text": process_text(
                TextKeys.homework_txt,
                callback,
                subject=subject,
                author=author_name,
                txt=txt,
                info="",
            ),
            "photos": [_["photo_id"] for _ in homework["photo_tg_id"]],
        }
        res.append(hw)
    if diary_data:
        for homework in diary_data["homework"]:
            hw = {
                "text": process_text(
                    TextKeys.homework_txt,
                    callback,
                    subject=homework["subject"],
                    author=diary_data["author"]["name"],
                    txt=homework["text"],
                    info="Получено из электронного дневника",
                ),
                "photos": [],
            }
            res.append(hw)
    return res

    # {предмет: [{txt: txt, photo: [photos]}]}


async def delete_msg(msg, time=10):
    await sleep(time)
    await msg.delete()


def convert_users(data):
    txt = "\n".join(
        [
            "Панель управления классом⭐️",
            "Список одноклассников:",
            *["@" + data[i] for i in data.keys()],
        ]
    )
    return txt


def make_username(user):
    # return f"@{user['first_name']}_{user['last_name']}_{user['id']}"
    if user["username"]:
        return f"@{user['username']}"
    else:
        fname = user["first_name"]
        lname = user["last_name"]
        if lname and fname:
            return f"{fname} {lname}"
        elif fname:
            return f"{fname}"
        elif lname:
            return f"{lname}"


def parse_args(string: str) -> list:
    """Разбивает строку на аргументы"""
    args = string.split(":")
    res = {}
    for i in args:
        arg = i.split("=")
        res[arg[0]] = arg[1]


def get_seconds_to_event(event_time) -> int:
    now = datetime.datetime.now()
    event_time = datetime.datetime.combine(now.date(), event_time)
    if event_time < now:
        event_time += datetime.timedelta(days=1)
    return (event_time - now).seconds