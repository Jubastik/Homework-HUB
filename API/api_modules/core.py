import datetime
import io
import base64
from PIL import Image
from random import randint
from tkinter import Image

from API.data import db_session
from API.data.classes import Class
from API.data.schedules import Schedule
from API.data.students import Student
from API.data.CONSTANTS import day_id_to_weekday
from API.data.week_days import WeekDay

TG = 'tg'


class IDError(Exception):
    pass


def id_processing(platform, id):
    db_sess = db_session.create_session()
    if platform == TG:
        id = db_sess.query(Student.id).filter(Student.tg_id == id).first()
    elif platform == 'no':
        id = db_sess.query(Student.id).filter(Student.id == id).first()
    else:
        raise IDError('Платформа не поддерживается')
    if id is None:
        raise IDError('Ошибка в ID')
    return id[0]


def generate_token():
    return randint(10000, 99999)


def get_next_lesson(class_id, lesson):
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
        schedules = db_sess.query(Schedule).join(WeekDay).filter(Schedule.class_id == class_id,
                                                                 WeekDay.name == day_id_to_weekday[
                                                                     weekday]).all()
        for schedule in schedules:
            if schedule.lesson.name == lesson:
                return now_date + datetime.timedelta(days=count)
    return None


def day_to_weekday(day):
    day_id = day.weekday()
    return day_id_to_weekday[day_id]


def decode_image(im_b64):
    img_bytes = base64.b64decode(im_b64.encode('utf-8'))
    img = Image.open(io.BytesIO(img_bytes))
    return img


def encode_image(image_path):
    with open(image_path, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    return im_b64
