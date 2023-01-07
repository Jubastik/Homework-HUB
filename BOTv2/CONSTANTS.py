import os

SUBJECTS = [
    "Русский🇷🇺",
    "Литература📚",
    "Алгебра🔢",
    "Геометрия📐",
    "Биология🌿",
    "География🌐",
    "История🗿",
    "Обществознание⚖",
    "Химия🧪",
    "Физкультура⚽",
    "English🇬🇧",
    "Физика⚡",
    "Информатика📡",
    "ОБЖ🪖",
    "Астрономия🔭",
    "Разговоры о важном🗣",
]
TG_BOT_LINK = "t.me/homework_hub_bot?start="
TG_OFFICAL_CHANNEL = "@Homework_bot_HUB"
URL_PARAM = f"?root_token={os.getenv('API_TOKEN', 'root')}"
SERVER = os.getenv("API_SERVER")  # при работе с url в следующий раз, сделать рефактор
URL_USER = SERVER + "/api/user"
URL_CHAT = SERVER + "/api/chats"
URL_CLASS = SERVER + "/api/class"
URL_SCHEDULE = SERVER + "/api/schedule"
URL_HOMEWORK = SERVER + "/api/homework"
URL_TIME_TABLE = SERVER + "/api/time_table"
URL_BAN_LIST = SERVER + "/api/ban_list"
URL_CURRENT_LESSONS = SERVER + "/api/current_lessons"
WEEKDAYS = {
    0: "понедельник",
    1: "вторник",
    2: "среда",
    3: "четверг",
    4: "пятница",
    5: "суббота",
    6: "воскресенье",
}
WEEKDAYS_TRASNLATE = {
    "понедельник": "monday",
    "вторник": "tuesday",
    "среда": "wednesday",
    "четверг": "thursday",
    "пятница": "friday",
    "суббота": "saturday",
    "воскресенье": "sunday",
}
