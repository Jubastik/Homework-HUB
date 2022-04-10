from random import randint

from API.data import db_session
from API.data.students import Student

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
