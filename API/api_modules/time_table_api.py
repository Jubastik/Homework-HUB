import datetime

import flask
import sqlalchemy
from flask import request, jsonify, make_response

from API.api_modules.core import id_processing, IDError
from API.data import db_session
from API.data.students import Student
from API.data.time_tables import TimeTable

blueprint = flask.Blueprint(
    'time_table',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/time_table', methods=['POST'])
def create_time_table():  # Создает расписание на основе входящего Json
    data = request.json
    if not data:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    elif not all(
            key in request.json for key in
            ["creator_id", "creator_platform", "lesson_number", "begin_time", "end_time"]):
        return make_response(jsonify(
            {
                'error': 'Отсутствуют поля "creator_id", "creator_platform", "lesson_number", "begin_time", "end_time"'}),
            422)
    try:
        creator_id = id_processing(data['creator_platform'], data['creator_id'])
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)

    db_sess = db_session.create_session()
    class_id = db_sess.query(Student.class_id).filter(Student.id == creator_id).first()
    if class_id is None:
        return make_response(jsonify({'error': f'Пользователь не состоит в классе'}), 422)
    else:
        class_id = class_id[0]
    if len(data['begin_time'].split(':')) != 2 or len(data['end_time'].split(':')) != 2:
        return make_response(jsonify({'error': 'Неверный формат времени'}), 422)
    b_h = int(data['begin_time'].split(':')[0])
    b_m = int(data['begin_time'].split(':')[1])
    e_h = int(data['end_time'].split(':')[0])
    e_m = int(data['end_time'].split(':')[1])
    begin_time = datetime.time(b_h, b_m)
    end_time = datetime.time(e_h, e_m)
    time_table = TimeTable(
        class_id=class_id,
        number_of_lesson=data['lesson_number'],
        begin_time=begin_time,
        end_time=end_time
    )
    db_sess.add(time_table)
    try:
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Слот уже существует'}), 422)
    return make_response(jsonify({'success': 'Слот успешно создан'}), 201)
