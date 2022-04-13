import flask
from flask import request, jsonify, abort, make_response

from API.api_modules.core import id_processing, IDError
from API.data import db_session
from API.data.lessons import Lesson
from API.data.schedules import Schedule
from API.data.students import Student
from API.data.time_tables import TimeTable
from API.data.week_days import WeekDay

blueprint = flask.Blueprint(
    'schedule',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/schedule/<int:tg_id>', methods=['GET'])
def get_schedule(tg_id):  # Возвращает все расписание
    return "get_schedule"


@blueprint.route('/api/schedule/<platform>/<int:user_id>/<day>', methods=['GET'])
def get_schedule_day(platform, user_id, day):  # Возвращает расписание на день
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    schedule = db_sess.query(Schedule).join(WeekDay).filter(WeekDay.name == day).first()
    return jsonify({'data': schedule.to_dict(only=('id', 'day_id', 'lesson.name', 'slot.number_of_lesson'))})


@blueprint.route('/api/schedule/', methods=['POST'])
def create_schedule():  # Создает расписание на основе входящего Json
    data = request.json
    if not data:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    elif not all(
            key in request.json for key in
            ["creator_id", "creator_platform", "day", "lesson_number", "lesson"]):
        return make_response(jsonify(
            {
                'error': 'Отсутствуют поля "creator_id", "creator_platform", "day", "lesson_number", "lesson"'}),
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

    day_id = db_sess.query(WeekDay.id).filter(WeekDay.name == data['day']).first()
    lessons_id = db_sess.query(Lesson.id).filter(Lesson.name == data['lesson']).first()
    slot_id = db_sess.query(TimeTable.id).filter(TimeTable.class_id == class_id,
                                                 TimeTable.number_of_lesson == data['lesson_number']).first()

    if slot_id is None:
        return make_response(jsonify({'error': f'У класса отсутствует временной слот {data["lesson_number"]}'}), 422)
    else:
        slot_id = slot_id[0]
    if day_id is None:
        day = WeekDay(day=data['day'])
        db_sess.add(day)
        db_sess.flush()
        day_id = day.id
    else:
        day_id = day_id[0]
    if lessons_id is None:
        lesson = Lesson(name=data['lesson'])
        db_sess.add(lesson)
        db_sess.flush()
        lessons_id = lesson.id
    else:
        lessons_id = lessons_id[0]

    schedule = Schedule(
        class_id=class_id,
        day_id=day_id,
        slot_id=slot_id,
        lesson_id=lessons_id,
    )
    db_sess.add(schedule)
    db_sess.commit()
    return make_response()


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['PUT'])
def full_edit_schedule(tg_id, day):  # Полное Изменение расписания на основе входящего Json
    return "full edit_schedule"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['PATCH'])
def edit_schedule(tg_id, day):  # Изменение расписания на основе входящего Json
    return "edit_schedule"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['DELETE'])
def del_schedule(tg_id, day):  # Удаление расписание
    return "del_schedule"
