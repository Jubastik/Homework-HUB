import flask
import sqlalchemy
from flask import request, make_response, jsonify

from api_modules.core import chat_id_processing, IDError
from data import db_session
from data.classes import Class
from data.students import Student
from data.chats import Chat

blueprint = flask.Blueprint("chat", __name__, template_folder="templates")


@blueprint.route("/api/chats/<platform>/<chat_id>", methods=["GET"])
def get_chat(platform, chat_id):  # Возвращает группу
    try:
        id = chat_id_processing(platform, chat_id)
    except IDError as e:
        return make_response(jsonify({"error": str(e)}), 404)
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = chat.to_dict(only=("tg_id", "class_id"))
    return jsonify({"data": data})


@blueprint.route("/api/chats", methods=["POST"])
def register_chat():  # Регистрация группы
    if not request.json:
        return make_response(jsonify({"error": "Пустой json"}), 400)
    if "user_tg_id" not in request.json or "chat_tg_id" not in request.json:
        return make_response(
            jsonify({"error": 'Отсутствует поле "user_tg_id" или "chat_tg_id"'}), 422
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
    chat = Chat(tg_id=data["chat_tg_id"], class_id=class_id)
    db_sess.add(chat)
    try:
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({"error": "Беседа уже зарегестрирована"}), 422)
    return make_response(jsonify({"success": "Беседа успешно зарегестрирована"}), 201)


@blueprint.route("/api/chats/<platform>/<chat_id>", methods=["DELETE"])
def delete_chat(platform, chat_id):  # Удаление группы
    try:
        id = chat_id_processing(platform, chat_id)
    except IDError as e:
        return make_response(jsonify({"error": str(e)}), 404)
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    db_sess.delete(chat)
    db_sess.commit()
    return make_response(jsonify({"success": "Беседа успешно удалена"}), 200)
