import flask

blueprint = flask.Blueprint(
    'schedule',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/schedule/<int:tg_id>', methods=['GET'])
def get_schedule(tg_id):  # Возвращает все расписание
    return "get_schedule"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['GET'])
def get_schedule_day(tg_id, day):  # Возвращает расписание на день
    return "get_schedule_day"


@blueprint.route('/api/schedule/<int:tg_id>', methods=['POST'])
def create_schedule(tg_id):  # Создает расписание на основе входящего Json
    return "create_schedule"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['PUT'])
def edit_schedule(tg_id, day):  # Изменение расписания на основе входящего Json
    return "edit_schedule"


@blueprint.route('/api/schedule/<int:tg_id>/<int:day>', methods=['DELETE'])
def del_schedule(tg_id, day):  # Удаление расписание
    return "del_schedule"
