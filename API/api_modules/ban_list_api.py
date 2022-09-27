import flask
import sqlalchemy
from flask import request, make_response, jsonify

from api_modules.core import user_id_processing, access_verification
from data import db_session
from data.classes import Class
from data.students import Student
from data.ban_list import Ban_list

blueprint = flask.Blueprint("ban_list", __name__, template_folder="templates")

@blueprint.route("/api/ban_list/<platform>/<userid>", methods=["GET"], endpoint="ban_list")
@access_verification
def get_banned_user(platform, userid):
    id = user_id_processing(platform, userid)
    db_sess = db_session.create_session()
    banned_user = db_sess.query(Ban_list).filter(Ban_list.id == id).first()
    res = banned_user.to_dict(only=("tg_id", "class_id"))
    db_sess.close()
    return jsonify({"data": res})


@blueprint.route("/api/ban_list", methods=["POST"], endpoint="add_ban")
@access_verification
def add_ban():
    if not request.json:
        return make_response(jsonify({"error": "Пустой json"}), 400)
    if "user_tg_id" not in request.json:
        return make_response(
            jsonify({"error": 'Отсутствует поле "user_tg_id""'}), 422
        )
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
    ban = Ban_list(tg_id=data["user_tg_id"], class_id=class_id)
    db_sess.add(ban)
    db_sess.commit()
    db_sess.close()
    return make_response(jsonify({"success": "Пользователь успешно добавлен в бан-лист"}), 201)