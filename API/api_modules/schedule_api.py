import flask
import sqlalchemy
from api_modules.core import IDError, access_verification, user_id_processing
from data import db_session
from data.classes import Class
from data.lessons import Lesson
from data.schedules import Schedule
from data.students import Student
from data.time_tables import TimeTable
from data.week_days import WeekDay
from flask import jsonify, make_response, request

blueprint = flask.Blueprint("schedule", __name__, template_folder="templates")


@blueprint.route("/api/schedule/<platform>/<int:user_id>", methods=["GET"], endpoint="schedule")
@access_verification
def get_schedule(platform, user_id):  # Возвращает все расписание
    id = user_id_processing(platform, user_id)
    db_sess = db_session.create_session()
    schedules = (
        db_sess.query(Schedule).join(Class).join(Student).filter(Student.id == id).all()
    )
    return_data = [
        schedule.to_dict(
            only=("day.name", "lesson.name", "slot.number_of_lesson")
        )
        for schedule in schedules
    ]
    db_sess.close()
    return jsonify({"data": return_data})


@blueprint.route("/api/schedule/<platform>/<int:user_id>/<day>", methods=["GET"], endpoint="schedule_day")
@access_verification
def get_schedule_day(platform, user_id, day):  # Возвращает расписание на день
    id = user_id_processing(platform, user_id)
    db_sess = db_session.create_session()
    schedules = (
        db_sess.query(Schedule)
        .join(WeekDay)
        .join(Class)
        .join(Student)
        .filter(Student.id == id, WeekDay.name == day.lower())
        .all()
    )
    return_data = [
        schedule.to_dict(only=("lesson.name", "slot.number_of_lesson"))
        for schedule in schedules
    ]
    db_sess.close()
    if len(schedules) == 0:
        return make_response(
            jsonify({"error": "Расписание на этот день не существует"}), 404
        )
    return jsonify({"data": return_data})


@blueprint.route("/api/schedule", methods=["POST"], endpoint="schedule_add")
@access_verification
def create_schedule():  # Создает расписание на основе входящего Json
    data = request.json
    if not data:
        return make_response(jsonify({"error": "Пустой json"}), 400)
    elif not all(
            key in request.json
            for key in ["creator_id", "creator_platform", "day", "lesson_number", "lesson"]
    ):
        return make_response(
            jsonify(
                {
                    "error": 'Отсутствуют поля "creator_id", "creator_platform", "day", "lesson_number", "lesson"'
                }
            ),
            422,
        )
    try:
        creator_id = user_id_processing(data["creator_platform"], data["creator_id"])
    except IDError as e:
        return make_response(jsonify({"error": str(e)}), 404)

    db_sess = db_session.create_session()
    class_id = db_sess.query(Student.class_id).filter(Student.id == creator_id).first()
    if class_id is None:
        db_sess.close()
        return make_response(
            jsonify({"error": f"Пользователь не состоит в классе"}), 422
        )
    else:
        class_id = class_id[0]
    day_id = (
        db_sess.query(WeekDay.id)
        .filter(WeekDay.name == str(data["day"]).lower())
        .first()
    )
    lessons_id = db_sess.query(Lesson.id).filter(Lesson.name == data["lesson"]).first()
    slot_id = (
        db_sess.query(TimeTable.id)
        .filter(
            TimeTable.class_id == class_id,
            TimeTable.number_of_lesson == data["lesson_number"],
        )
        .first()
    )

    if slot_id is None:
        db_sess.close()
        return make_response(
            jsonify(
                {
                    "error": f'У класса отсутствует временной слот {data["lesson_number"]}'
                }
            ),
            422,
        )
    else:
        slot_id = slot_id[0]
    if day_id is None:
        db_sess.close()
        return make_response(jsonify({"error": f'Неизвестный день {data["day"]}'}), 422)
    else:
        day_id = day_id[0]
    if lessons_id is None:
        lesson = Lesson(name=data["lesson"])
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
    try:
        db_sess.commit()
        db_sess.close()
    except sqlalchemy.exc.IntegrityError:
        db_sess.close()
        return make_response(jsonify({"error": "Расписание уже существует"}), 422)
    return make_response(jsonify({"success": f"Расписание успешно создано."}), 201)


@blueprint.route("/api/schedule/study_days/<platform>/<int:user_id>", methods=["GET"], endpoint="get_study_days")
@access_verification
def get_study_days(platform, user_id):
    id = user_id_processing(platform, user_id)
    db_sess = db_session.create_session()
    schedules = (
        db_sess.query(Schedule).join(Class).join(Student).filter(Student.id == id).all()
    )
    res = set()
    for i in schedules:
        res.add(i.day.name)
    return jsonify({"data": list(res)})