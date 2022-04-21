import flask
import sqlalchemy
from flask import request, jsonify, make_response

from API.api_modules.core import id_processing, IDError
from API.data import db_session
from API.data.classes import Class
from API.data.students import Student

blueprint = flask.Blueprint(
    'user',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/<platform>/<int:user_id>', methods=['GET'])
def get_user(platform, user_id):  # Возвращает базовую информацию о пользователе
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    return jsonify({'data': student.to_dict(only=('id', 'name', 'class_id', 'is_admin'))})


@blueprint.route('/api/user', methods=['POST'])
def create_user():  # Создает пользователя на основе входящего Json
    # получить тело с tg_id
    if not request.json:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    elif not all(key in request.json for key in
                 ["platform", "id", "name"]):
        return make_response(jsonify({'error': 'Отсутствуют поля "platform", "id", "name"'}), 422)
    db_sess = db_session.create_session()  # добавить регу по токену
    data = request.json
    class_id = None
    if "class_token" in data:
        class_id = db_sess.query(Class.id).filter(Class.class_token == data["class_token"]).first()
        if class_id is not None:
            class_id = class_id[0]
        else:
            return make_response(jsonify({'error': 'Нет такого класса'}), 404)
    if data['platform'] == "tg":
        student = Student(
            tg_id=data['id'],
            name=data['name'],
            class_id=class_id
        )
    else:
        return make_response(jsonify({'error': 'поддерживается только tg'}), 422)
    db_sess.add(student)
    try:
        db_sess.commit()
    except sqlalchemy.exc.IntegrityError:
        return make_response(jsonify({'error': 'Такой пользователь уже существует'}), 400)
    return make_response()


# {
#     platform:
#     id:
#     name:
# }

@blueprint.route('/api/user/<platform>/<int:user_id>', methods=['PUT'])
def full_edit_user(platform, user_id):  # Полное Изменение пользователя на основе входящего Json
    return "full edit_user"


@blueprint.route('/api/user/<platform>/<int:user_id>', methods=['PATCH'])
def edit_user(platform, user_id):  # Изменение пользователя на основе входящего Json
    if not request.json:
        return make_response(jsonify({'error': 'Пустой json'}), 400)
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).filter(Student.id == id).first()
    data = request.json
    for key, data in data.items():
        if key == "name":
            student.name = data
        elif key == "class_id":
            student.class_id = data
        elif key == "is_admin":
            student.is_admin = data
        else:
            return make_response(jsonify({'error': f'Неизвестный параметр {key}'}), 422)
    db_sess.commit()
    return make_response()


@blueprint.route('/api/user/<platform>/<int:user_id>', methods=['DELETE'])
def del_user(platform, user_id):  # Удаление пользователя
    try:
        id = id_processing(platform, user_id)
    except IDError as e:
        return make_response(jsonify({'error': str(e)}), 404)
    db_sess = db_session.create_session()
    student = db_sess.query(Student).get(id)
    if student.class_id is not None:
        admins_in_class = db_sess.query(Student).join(Class).filter(Class.id == student.class_id,
                                                                    Student.is_admin == True).count()
        if admins_in_class == 1:
            return make_response(jsonify({'error': 'Нельзя удалить последнего админа'}), 422)
    db_sess.delete(student)
    db_sess.commit()
    return make_response('', 204)
