import datetime

import flask
import sqlalchemy
from flask import request, jsonify, make_response

from api_modules.core import (
    user_id_processing,
    IDError,
    get_next_lesson,
    day_to_weekday,
    chat_id_processing, access_verification,
)
from data import db_session
from data.classes import Class
from data.homeworks import Homework
from data.lessons import Lesson
from data.schedules import Schedule
from data.students import Student
from data.tg_photos import TgPhoto
from data.week_days import WeekDay
from data.chats import Chat

blueprint = flask.Blueprint("homework", __name__, template_folder="templates")


@blueprint.route("/api/homework/<platform>/<int:user_id>/<date>", methods=["GET"], endpoint='homework')
@access_verification
def get_homework_date(platform, user_id, date):  # Возвращает дз на дату
    is_chat = request.args.get("is_chat", default="False") != "False"
    if is_chat:
        # HTTP не одобряет отрицательные числа (вернее знак "-") НО! в telegram id чата это отрицательное число
        user_id *= -1
        id = chat_id_processing(platform, user_id)
    else:
        id = user_id_processing(platform, user_id)
    if len(date.split("-")) != 3:
        return make_response(
            jsonify({"error": "Формат даты должен быть день-месяц-год"}), 422
        )
    day, month, year = date.split("-")
    date = datetime.date(int(year), int(month), int(day))
    db_sess = db_session.create_session()
    if not is_chat:
        homeworks = (
            db_sess.query(Homework)
            .join(Schedule)
            .join(Class)
            .join(Student)
            .filter(Student.id == id, Homework.date == date)
            .all()
        )
    else:
        homeworks = (
            db_sess.query(Homework)
            .join(Schedule)
            .join(Class)
            .join(Student)
            .join(Chat)
            .filter(Chat.id == id, Homework.date == date)
            .all()
        )
    db_sess.close()
    if len(homeworks) == 0:
        return make_response(
            jsonify({"error": "Нет домашнего задания на эту дату"}), 404
        )
    return jsonify(
        {
            "data": [
                homework.to_dict(
                    only=(
                        "text_homework",
                        "photo_tg_id.photo_id",
                        "schedule.lesson.name",
                        "schedule.slot.number_of_lesson",
                        "author_id",
                    )
                )
                for homework in homeworks
            ]
        }
    )


@blueprint.route("/api/homework", methods=["POST"], endpoint='add_homework')
@access_verification
def create_homework():  # Создает дз на основе входящего Json
    data = request.json
    if not data:
        return make_response(jsonify({"error": "Пустой json"}), 400)
    elif not all(
        key in data for key in ["creator_id", "creator_platform", "lesson", "date"]
    ):
        return make_response(
            jsonify(
                {
                    "error": 'Отсутствуют поля "creator_id", "creator_platform", "lesson", "date"'
                }
            ),
            422,
        )
    elif "photo" not in data and "text" not in data and "photos_tg_id" not in data:
        return make_response(
            jsonify(
                {"error": 'Отсутствуют поля "photo" или "text" или "photos_tg_id"'}
            ),
            422,
        )
    creator_id = user_id_processing(data["creator_platform"], data["creator_id"])
    db_sess = db_session.create_session()
    my_class = db_sess.query(Student.class_id).filter(Student.id == creator_id).first()
    if my_class is None:
        db_sess.close()
        return make_response(jsonify({"error": "У пользователя нет класса"}), 422)
    else:
        my_class = my_class[0]
    if data["date"] == "auto":
        date = get_next_lesson(my_class, data["lesson"])
        if date is None:
            db_sess.close()
            return make_response(
                jsonify({"error": f'Авто дата не нашла урок. {data["lesson"]}'}), 422
            )
    else:
        if len(data["date"].split("-")) != 3:
            db_sess.close()
            return make_response(
                jsonify({"error": "Формат даты должен быть день-месяц-год"}), 422
            )
        day, month, year = data["date"].split("-")
        date = datetime.date(int(year), int(month), int(day))
    if date < datetime.datetime.now().date():
        db_sess.close()
        return make_response(jsonify({"error": "Дата уже прошла"}), 422)
    day_of_week = day_to_weekday(date)
    if day_of_week == 'воскресенье':
        db_sess.close()
        return make_response(jsonify({"error": "Нельзя добавлять дз в воскресенье"}), 422)
    schedule_id = (
        db_sess.query(Schedule.id)
        .join(WeekDay)
        .join(Lesson)
        .filter(
            WeekDay.name == day_of_week,
            Schedule.class_id == my_class,
            Lesson.name == data["lesson"],
        )
        .first()
    )
    if schedule_id is None:
        db_sess.close()
        return make_response(
            jsonify(
                {
                    "error": f'Нет урока в этот день. Урок:{data["lesson"]} День:{day_of_week}'
                }
            ),
            422,
        )
    else:
        schedule_id = schedule_id[0]
    if "text" in data:
        homework = Homework(
            author_id=creator_id,
            date=date,
            schedule_id=schedule_id,
            text_homework=data["text"],
        )
    else:
        homework = Homework(author_id=creator_id, date=date, schedule_id=schedule_id)
    db_sess.add(homework)
    db_sess.flush()
    if "photos_tg_id" in data:
        for photo_tg_id in data["photos_tg_id"]:
            tg_p = TgPhoto(homework_id=homework.id, photo_id=photo_tg_id)
            db_sess.add(tg_p)
    if "photo" in data:
        db_sess.close()
        return make_response(
            jsonify({"error": 'Отправка фото пока что недоступна"'}), 422
        )
    db_sess.commit()
    db_sess.close()
    return make_response(
        jsonify({"success": f'ДЗ создано. Дата:{date}, Урок:{data["lesson"]}'}), 201
    )
