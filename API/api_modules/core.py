import datetime
import os
from random import randint

from flask import make_response, jsonify, request

from data import db_session
from data.chats import Chat
from data.schedules import Schedule
from data.students import Student
from CONSTANTS import day_id_to_weekday
from data.week_days import WeekDay

TG = "tg"
NO = "no"


class IDError(Exception):
    pass


def access_verification(func):
    def wrapper(*args, **kwargs):
        if request.args.get('root_token', type=str) is not None:
            if request.args.get('root_token', type=str) == os.getenv('ROOT_TOKEN', "root"):
                return func(*args, **kwargs)
            else:
                return make_response(jsonify({'error': 'Неверный токен'}), 401)
        else:
            return make_response(jsonify({'error': 'Отсутствует токен'}), 401)
    return wrapper


def user_id_processing(platform, id):
    db_sess = db_session.create_session()
    if platform == TG:
        id = db_sess.query(Student.id).filter(Student.tg_id == id).first()
    elif platform == NO:
        id = db_sess.query(Student.id).filter(Student.id == id).first()
    else:
        db_sess.close()
        raise IDError("Платформа не поддерживается")
    db_sess.close()
    if id is None:
        raise IDError("Несуществующий пользователь")
    return id[0]


def chat_id_processing(platform, id):
    db_sess = db_session.create_session()
    if platform == TG:
        id = db_sess.query(Chat.id).filter(Chat.tg_id == id).first()
    elif platform == NO:
        id = db_sess.query(Chat.id).filter(Chat.id == id).first()
    else:
        db_sess.close()
        raise IDError("Платформа не поддерживается")
    db_sess.close()
    if id is None:
        raise IDError("Несуществующий пользователь")
    return id[0]


def generate_token():
    return randint(10000, 99999)


def get_next_lesson(class_id, lesson):
    """
    Получение дня недели, в котором присутствует необходимый нам урок
    """
    now_date = datetime.date.today()
    weekday = datetime.datetime.today().weekday()
    count = 0
    while count != 7:
        count += 1
        weekday += 1
        if weekday == 6:
            continue
        elif weekday == 7:
            weekday = 0

        db_sess = db_session.create_session()
        schedules = (
            db_sess.query(Schedule)
            .join(WeekDay)
            .filter(
                Schedule.class_id == class_id,
                WeekDay.name == day_id_to_weekday[weekday],
            )
            .all()
        )
        for schedule in schedules:
            if schedule.lesson.name == lesson:
                return now_date + datetime.timedelta(days=count)
    return None


def day_to_weekday(day):
    """
    Конвертация дня недели в название дня недели
    """
    day_id = day.weekday()
    return day_id_to_weekday[day_id]
