from flask import Flask

from API.data import db_session
from API.data.classes import Class
from API.data.students import Student
from api_modules import user_api, homework_api, class_api, schedule_api

app = Flask(__name__)


def main():
    db_session.global_init("db/API.db")
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(homework_api.blueprint)
    app.register_blueprint(class_api.blueprint)
    app.register_blueprint(schedule_api.blueprint)
    app.run(debug=True)


@app.route('/test')
def hello_world():  # put application's code here
    db_sess = db_session.create_session()
    class_id = 7
    users = db_sess.query(Student).where(Student.class_id == class_id).first()
    print(users)
    return 'Hello World!'


if __name__ == '__main__':
    main()
