import io
import base64
from PIL import Image
from random import randint
from tkinter import Image

from API.data import db_session
from API.data.students import Student
from API.data.CONSTANTS import day_id_to_weekday

TG = 'tg'


class IDError(Exception):
    pass


def id_processing(platform, id):
    if platform == TG:
        db_sess = db_session.create_session()
        id = db_sess.query(Student.id).filter(Student.tg_id == id).first()
        if id is None:
            raise IDError('Ошибка в ID')
        return id[0]
    elif platform == 'no':
        db_sess = db_session.create_session()
        id = db_sess.query(Student.id).filter(Student.id == id).first()
        if id is None:
            raise IDError('Ошибка в ID')
        return id[0]
    else:
        raise IDError('Платформа не поддерживается')


def generate_token():
    return randint(10000, 99999)


def get_next_lesson(class_id, lesson):
    pass


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
