import os

from dotenv import load_dotenv
from flask import Flask, jsonify

from api_modules.core import IDError
from data import db_session
from CONSTANTS import day_id_to_weekday
from data.week_days import WeekDay
from api_modules import (
    user_api,
    homework_api,
    class_api,
    schedule_api,
    time_table_api,
    additional_methods_api,
    chat_api
)

load_dotenv()

app = Flask(__name__)


def main():
    """Регистрация модулей и запуск приложения"""
    db_session.global_init()
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(homework_api.blueprint)
    app.register_blueprint(class_api.blueprint)
    app.register_blueprint(schedule_api.blueprint)
    app.register_blueprint(time_table_api.blueprint)
    app.register_blueprint(additional_methods_api.blueprint)
    app.register_blueprint(chat_api.blueprint)
    init_weekday()
    app.run(host=os.getenv("API_HOST", ""), port=os.getenv('API_PORT', 8000),
            debug=os.getenv("API_DEBUG", False) == 'True')


@app.route("/")
def hello_world():
    return "Hello HomeBot!!"


@app.errorhandler(IDError)
def handle_id_error_request(e):
    return jsonify(error=str(e)), 404

def init_weekday():
    """Инициализация дней недели в бд"""
    db_sess = db_session.create_session()
    for weekday in day_id_to_weekday.values():
        wd = WeekDay(name=weekday)
        db_sess.add(wd)
        try:
            db_sess.commit()
        except Exception as e:
            pass
    return "OK"

if __name__ == "__main__":
    main()
