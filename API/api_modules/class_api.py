import flask

blueprint = flask.Blueprint(
    'class',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/class/<int:tg_id>/<int:class_id>', methods=['GET'])
def get_class(tg_id, class_id):  # Возвращает токен класса, vk_id класса и tg_id пользователей
    return "get_class"


@blueprint.route('/api/schedule/<int:tg_id>', methods=['POST'])
def create_class(tg_id):  # Создает класс на основе входящего Json
    return "create_class"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['PUT'])
def edit_class(tg_id, day):  # Изменение класс на основе входящего Json (изменение токена, vk_id)
    return "edit_class"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['DELETE'])
def del_class(tg_id, day):  # Удаление класс
    return "del_class"
