from flask import Flask, make_response
from API.data import db_session
from API.data.CONSTANTS import day_id_to_weekday
from API.data.classes import Class
from API.data.students import Student
from API.data.week_days import WeekDay
from api_modules import user_api, homework_api, class_api, schedule_api, time_table_api, additional_methods_api

app = Flask(__name__)


def main():
    db_session.global_init("db/API.db")
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(homework_api.blueprint)
    app.register_blueprint(class_api.blueprint)
    app.register_blueprint(schedule_api.blueprint)
    app.register_blueprint(time_table_api.blueprint)
    app.register_blueprint(additional_methods_api.blueprint)
    app.run(debug=True)
    init_weekday()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/init_weekday')
def init_weekday():
    db_sess = db_session.create_session()
    for weekday in day_id_to_weekday.values():
        wd = WeekDay(name=weekday)
        db_sess.add(wd)
        try:
            db_sess.commit()
        except IndentationError as e:
            pass
    return make_response('OK')


if __name__ == '__main__':
    main()
