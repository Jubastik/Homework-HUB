import flask
from flask import request, make_response, jsonify

from API.api_modules.core import id_processing, generate_token, IDError
from API.data import db_session
from API.data.classes import Class
from API.data.students import Student

blueprint = flask.Blueprint(
    'class',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/class/<platform>/<int:user_id>', methods=['GET'])
def get_class(platform, user_id):  # Возвращает токен класса, vk_id класса и tg_id пользователей
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    my_class = student.my_class
    return jsonify({'data': my_class.to_dict(only=('id', 'name', 'class_token', 'vk_id', 'student.id'))})


@blueprint.route('/api/class', methods=['POST'])
def create_class():  # Создает класс на основе входящего Json
    if not request.json:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    elif not all(key in request.json for key in ["creator_platform", "creator_id", "name"]):
        return make_response(jsonify({'error': 'Отсутствуют поля "creator_platform", "creator_id", "name"'}), 422)
    data = request.json

    try:
        creator_id = id_processing(data['creator_platform'], data['creator_id'])
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)

    db_sess = db_session.create_session()
    my_class = Class(
        name=data['name'],
        class_token=generate_token()
    )

    db_sess.add(my_class)

    student = db_sess.query(Student).filter(Student.id == creator_id).first()
    student.is_admin = True
    student.class_id = my_class.id
    db_sess.commit()
    return make_response()


@blueprint.route('/api/class/<platform>/<int:user_id>', methods=['PUT'])
def full_edit_class(tg_id, day):  # Полное Изменение класс на основе входящего Json (изменение токена, vk_id)
    return "full_edit_class"


@blueprint.route('/api/class/<platform>/<int:user_id>', methods=['PATCH'])
def edit_class(platform, user_id):  # Изменение класс на основе входящего Json (изменение токена, vk_id)
    json_data = request.json
    if not json_data:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    if not student.is_admin:
        return make_response(jsonify({'error': 'Нет прав'}), 404)
    my_class = student.my_class
    for key, data in json_data.items():
        if key == "class_token":
            my_class.class_token = data
        elif key == "vk_id":
            my_class.vk_id = data
        elif key == 'name':
            my_class.name = data
        else:
            return make_response(jsonify({'error': f'Неизвестный параметр {key}'}), 422)
    db_sess.commit()
    return make_response()


@blueprint.route('/api/class/<platform>/<int:user_id>', methods=['DELETE'])
def del_class(platform, user_id):  # Удаление класса
    return "del_class"
