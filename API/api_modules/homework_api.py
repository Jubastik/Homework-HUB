import flask

blueprint = flask.Blueprint(
    'homework',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/homework/<int:tg_id>', methods=['GET'])
def get_homework(tg_id):  # Возвращает дз на неделю
    return "get_homework"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['GET'])
def get_homework_date(tg_id, date):  # Возвращает дз на дату
    return "get_homework_date"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['POST'])
def create_homework(tg_id, date):  # Создает дз на основе входящего Json
    return "create_homework"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['PUT'])
def edit_homework(tg_id, date):  # Изменение дз на основе входящего Json
    return "edit_homework"


@blueprint.route('/api/homework/<int:tg_id>/<int:date>', methods=['DELETE'])
def del_homework(tg_id, date):  # Удаление дз
    return "del_homework"
