import os

SERVER = os.getenv("API_SERVER")
print(SERVER)
URL_STUDENT = SERVER + "/api2/student/"
URL_CLASS = SERVER + "/api2/class/"
URL_SCHEDULE = SERVER + "/api2/schedule/"
URL_CHAT = SERVER + "/api2/chats"
URL_HOMEWORK = SERVER + "/api2/homework/"
URL_BAN = SERVER + "/api2/ban/"
URL_PARSER = SERVER + "/api2/parser/"
URL_TIME_TABLE = SERVER + "/api2/time_table"
URL_CURRENT_LESSONS = SERVER + "/api2/current_lessons"