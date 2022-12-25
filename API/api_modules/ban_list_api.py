import flask
import sqlalchemy
from api_modules.core import access_verification, user_id_processing
from data import db_session
from data.ban_list import Ban_list
from data.classes import Class
from data.students import Student
from flask import jsonify, make_response, request

blueprint = flask.Blueprint("ban_list", __name__, template_folder="templates")


@blueprint.route(
    "/api/ban_list/<platform>/<userid>", methods=["GET"], endpoint="ban_list"
)
@access_verification
def get_banned_user(platform, userid):
    id = user_id_processing(platform, userid)
    db_sess = db_session.create_session()
    banned_user = db_sess.query(Ban_list).filter(Ban_list.id == id).first()
    res = banned_user.to_dict(only=("id", "tg_id", "class_id", "name"))
    db_sess.close()
    return jsonify({"data": res})


@blueprint.route("/api/ban_list", methods=["POST"], endpoint="add_ban")
@access_verification
def add_ban():
    if not request.json:
        return make_response(jsonify({"error": "Пустой json"}), 400)
    if "user_tg_id" not in request.json or "username" not in request.json:
        return make_response(jsonify({"error": 'Отсутствует поле "user_tg_id" или "username"'}), 422)
    data = request.json
    db_sess = db_session.create_session()
    class_id = (
        db_sess.query(Class.id)
        .join(Student)
        .filter(Student.tg_id == data["user_tg_id"])
        .first()
    )
    if class_id is not None:
        class_id = class_id[0]
    else:
        return make_response(jsonify({"error": "Пользователь не был найден."}), 404)
    ban = Ban_list(tg_id=data["user_tg_id"], class_id=class_id, name=data["username"])
    id = user_id_processing("tg", data["user_tg_id"])
    student = db_sess.query(Student).get(id)
    if student.is_admin is True:
        admins_in_class = (
            db_sess.query(Student)
            .join(Class)
            .filter(Class.id == student.class_id, Student.is_admin == True)
            .count()
        )
        students_in_class = (
            db_sess.query(Student)
            .join(Class)
            .filter(Class.id == student.class_id)
            .count()
        )
        if admins_in_class == 1 and students_in_class != 1:
            db_sess.close()
            return make_response(
                jsonify(
                    {"error": "Нельзя забанить последнего админа в классе с учениками"}
                ),
                422,
            )
    classmates_count = (
        db_sess.query(Student).join(Class).filter(Class.id == student.class_id).count()
    )
    db_sess.add(ban)
    if classmates_count == 1:
        db_sess.delete(student.my_class)
    else:
        db_sess.delete(student)
    try:
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        db_sess.close()
        return make_response(
            jsonify({"error": "Пользователь уже забанен в этом классе"}), 409
        )
    db_sess.close()
    return make_response(
        jsonify({"success": "Пользователь успешно добавлен в бан-лист"}), 201
    )


@blueprint.route("/api/ban_list/<id>", methods=["DELETE"], endpoint="delete_ban")
@access_verification
def delete_ban(id):
    db_sess = db_session.create_session()
    ban = db_sess.query(Ban_list).filter(Ban_list.id == id).first()
    db_sess.delete(ban)
    db_sess.commit()
    db_sess.close()
    return make_response(jsonify({"success": "Пользователь успешно разбанен"}), 200)


@blueprint.route(
    "/api/ban_list/class/<platform>/<userid>", methods=["GET"], endpoint="get_class_bans"
)
@access_verification
def get_class_ban_list(platform, userid):
    id = user_id_processing(platform, userid)
    db_sess = db_session.create_session()
    class_id = db_sess.query(Student.class_id).filter(Student.id == id).first()[0]
    ban_list = db_sess.query(Ban_list).filter(Ban_list.class_id == class_id).all()
    if len(ban_list) == 0:
        return make_response(jsonify({"error": "Бан-лист класса пуст"}), 404)
    res = [ban.to_dict(only=("id", "name", "tg_id")) for ban in ban_list]
    db_sess.close()
    return jsonify({"data": res})
