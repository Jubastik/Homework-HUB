import datetime

import flask
from flask import jsonify, make_response

from CONSTANTS import day_id_to_weekday
from api_modules.core import user_id_processing, IDError, access_verification
from data import db_session
from data.classes import Class
from data.schedules import Schedule
from data.students import Student
from data.time_tables import TimeTable
from data.week_days import WeekDay

blueprint = flask.Blueprint("additional", __name__, template_folder="templates")


@blueprint.route("/api/current_lessons/<platform>/<int:user_id>", methods=["GET"], endpoint="current_lessons")
@access_verification
def current_lessons(platform, user_id):
    """
    Получение названий  ближайших уроков
    """
    id = user_id_processing(platform, user_id)
    db_sess = db_session.create_session()

    now_time = datetime.datetime.now().time()
    past_time = datetime.datetime.combine(datetime.date.today(), now_time) - datetime.timedelta(minutes=60)
    past_time = past_time.time()
    day = day_id_to_weekday[datetime.datetime.today().weekday()]

    # now_time = datetime.time(13, 30)  # После отладки надо сделать нормально!!!!
    # past_time = datetime.time(10, 30)
    # day = "понедельник"

    now_lesson = (
        db_sess.query(Schedule)
            .join(WeekDay)
            .join(TimeTable)
            .join(Class)
            .join(Student)
            .filter(
            Student.id == id,
            WeekDay.name == day,
            TimeTable.begin_time >= past_time,
            TimeTable.end_time < now_time,
        )
            .all()
    )
    db_sess.close()
    if len(now_lesson) == 0:
        return make_response(
            jsonify({"error": "Ближайшие уроки не найдены"}), 404
        )
    return jsonify({"lessons": [_.to_dict(only=("lesson.name",)) for _ in now_lesson]})
