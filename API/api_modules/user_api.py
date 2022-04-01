import flask

blueprint = flask.Blueprint(
    'user',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/user/<int:tg_id>', methods=['GET'])
def get_user(tg_id):  # Возвращает базовую информацию о пользователе
    return "check_user"


@blueprint.route('/api/user/<int:tg_id>', methods=['POST'])
def create_user(tg_id):  # Создает пользователя на основе входящего Json
    return "create_user"


@blueprint.route('/api/user/<int:tg_id>', methods=['PUT'])
def edit_user(tg_id):  # Изменение пользователя на основе входящего Json
    return "edit_user"


@blueprint.route('/api/user/<int:tg_id>', methods=['DELETE'])
def del_user(tg_id):  # Удаление пользователя
    return "del_user"
