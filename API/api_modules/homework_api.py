import datetime

import flask
import sqlalchemy
from flask import request, jsonify, make_response

from API.api_modules.core import id_processing, IDError, get_next_lesson, day_to_weekday
from API.data import db_session
from API.data.classes import Class
from API.data.homeworks import Homework
from API.data.lessons import Lesson
from API.data.schedules import Schedule
from API.data.students import Student
from API.data.week_days import WeekDay

blueprint = flask.Blueprint(
    'homework',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/homework/<int:tg_id>', methods=['GET'])
def get_homework(tg_id):  # Возвращает дз на неделю
    return "get_homework"


@blueprint.route('/api/homework/<platform>/<int:user_id>/<date>', methods=['GET'])
def get_homework_date(platform, user_id, date):  # Возвращает дз на дату
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    day = date.split('-')[0]
    month = date.split('-')[1]
    year = date.split('-')[2]
    date = datetime.date(int(year), int(month), int(day))
    db_sess = db_session.create_session()
    homeworks = db_sess.query(Homework).join(Schedule).join(Class).join(Student).filter(Student.id == id,
                                                                                        Homework.date == date).all()
    if len(homeworks) == 0:
        return make_response(jsonify({'error': 'Нет домашнего задания на эту дату'}), 404)
    return jsonify({'data': [homework.to_dict(
        only=('text_homework', 'photo_tg_id', 'schedule.lesson.name', 'schedule.slot.number_of_lesson')) for
                             homework in homeworks]})


@blueprint.route('/api/homework', methods=['POST'])
def create_homework():  # Создает дз на основе входящего Json
    data = request.json
    if not data:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    elif not all(
            key in data for key in
            ["creator_id", "creator_platform", "lesson", "date"]):
        return make_response(jsonify(
            {
                'error': 'Отсутствуют поля "creator_id", "creator_platform", "lesson", "date"'}),
            422)
    elif 'photo' not in data and 'text' not in data and 'photo_tg_id' not in data:
        return make_response(jsonify(
            {'error': 'Отсутствуют поля "photo" или "text" или "photo_tg_id"'}), 422)
    try:
        creator_id = id_processing(data['creator_platform'], data['creator_id'])
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)

    db_sess = db_session.create_session()
    my_class = db_sess.query(Student.class_id).filter(Student.id == creator_id).first()
    if my_class is None:
        return make_response(jsonify({'error': 'У пользователя нет класса'}), 422)
    else:
        my_class = my_class[0]
    if data['date'] == 'auto':
        date = get_next_lesson(my_class, data['lesson'])
        if date is None:
            return make_response(jsonify({'error': f'Авто дата не нашла урок. {data["lesson"]}'}), 422)
    else:
        day = data['date'].split('-')[0]
        month = data['date'].split('-')[1]
        year = data['date'].split('-')[2]
        date = datetime.date(int(year), int(month), int(day))
    if date < datetime.datetime.now().date():
        return make_response(jsonify({'error': 'Дата уже прошла'}), 422)
    day_of_week = day_to_weekday(date)
    schedule_id = db_sess.query(Schedule.id).join(WeekDay).join(Lesson).filter(WeekDay.name == day_of_week,
                                                                               Schedule.class_id == my_class,
                                                                               Lesson.name == data['lesson']).first()
    if schedule_id is None:
        return make_response(jsonify({'error': f'Нет урока в этот день. Урок:{data["lesson"]} День:{day_of_week}'}),
                             422)
    else:
        schedule_id = schedule_id[0]
    if 'text' in data:
        homework = Homework(author_id=creator_id, date=date, schedule_id=schedule_id, text_homework=data['text'])
    elif 'photo_tg_id' in data:
        homework = Homework(author_id=creator_id, date=date, schedule_id=schedule_id, photo_tg_id=data['photo_tg_id'])
    else:
        return make_response(jsonify({'error': 'доработка"'}), 422)
    db_sess.add(homework)
    db_sess.commit()
    return make_response(jsonify({'success': f'ДЗ создано. Дата:{date}, Урок:{data["lesson"]}'}), 201)


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['PUT'])
def full_edit_homework(tg_id, date):  # Полное Изменение дз на основе входящего Json
    return "full edit_homework"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['PATCH'])
def edit_homework(tg_id, date):  # Изменение дз на основе входящего Json
    return "edit_homework"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['DELETE'])
def del_homework(tg_id, date):  # Удаление дз
    return "del_homework"
