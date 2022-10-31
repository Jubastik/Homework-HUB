import flask
import sqlalchemy
from api_modules.core import (access_verification, chat_id_processing,
                              user_id_processing)
from data import db_session
from data.chats import Chat
from data.classes import Class
from data.students import Student
from flask import jsonify, make_response, request

blueprint = flask.Blueprint("chat", __name__, template_folder="templates")


@blueprint.route("/api/chats/<platform>/<chat_id>", methods=["GET"], endpoint="chat")
@access_verification
def get_chat(platform, chat_id):  # Возвращает группу
    id = chat_id_processing(platform, chat_id)
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    data = chat.to_dict(only=("tg_id", "class_id", "mailing_time"))
    db_sess.close()
    return jsonify({"data": data})


@blueprint.route("/api/chats", methods=["POST"], endpoint="create_chat")
@access_verification
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
        db_sess.close()
        return make_response(jsonify({"error": "Беседа уже зарегестрирована"}), 422)
    db_sess.close()
    return make_response(jsonify({"success": "Беседа успешно зарегестрирована"}), 201)


@blueprint.route("/api/chats/<platform>/<chat_id>", methods=["DELETE"], endpoint="delete_chat")
@access_verification
def delete_chat(platform, chat_id):  # Удаление группы
    id = chat_id_processing(platform, chat_id)
    db_sess = db_session.create_session()
    chat = db_sess.query(Chat).filter(Chat.id == id).first()
    db_sess.delete(chat)
    db_sess.commit()
    db_sess.close()
    return make_response(jsonify({"success": "Беседа успешно удалена"}), 200)


@blueprint.route("/api/chats/all", methods=["GET"], endpoint="all_chats")
@access_verification
def get_chats():  # Возвращает все чаты, у которых включена рассылка
    db_sess = db_session.create_session()
    chats = db_sess.query(Chat).join(Class).filter(Chat.class_id == Class.id and Class.stop_mailing == False).all()
    data = [chat.to_dict(only=("tg_id", "class_id", "my_class.mailing_time")) for chat in chats]
    db_sess.close()
    return jsonify({"data": data})


@blueprint.route("/api/chats/by_user/<platform>/<user_id>", methods=["GET"], endpoint="chats_by_user")
@access_verification
def get_chats_by_userid(platform, user_id):  # Возвращает все чаты юзера
    id = user_id_processing(platform, user_id)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    class_id = student.my_class.id
    chats = db_sess.query(Chat).join(Class).filter(Chat.class_id == class_id and Class.stop_mailing == False).all()
    data = [chat.to_dict(only=("tg_id", "class_id", "my_class.mailing_time")) for chat in chats]
    db_sess.close()
    if len(data) == 0:
        return make_response(jsonify({"error": "У пользователя нет чатов"}), 404)
    return jsonify({"data": data})


# TODO:
# 1) Изменение времени отправки у класса ☑️
# 2) Получение всех чатов с включенной рассыкой ☑️
# 3) Включение выключение рассылки у класса ☑️