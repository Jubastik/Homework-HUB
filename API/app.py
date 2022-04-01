from flask import Flask
from api_modules import user_api, homework_api, class_api, schedule

app = Flask(__name__)


def main():
    app.register_blueprint(user_api.blueprint)
    app.register_blueprint(homework_api.blueprint)
    app.register_blueprint(class_api.blueprint)
    app.register_blueprint(schedule.blueprint)
    app.run()


@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'


if __name__ == '__main__':
    main()
