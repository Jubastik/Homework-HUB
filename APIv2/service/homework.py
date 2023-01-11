import datetime

from fastapi import Depends
from datetime import date
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.chats import Chat
from database.classes import Class
from database.db_session import get_session
from database.homeworks import Homework
from database.lessons import Lesson
from database.schedules import Schedule
from database.students import Student
from database.tg_photos import TgPhoto
from database.week_days import WeekDay
from my_err import APIError
from schemas.homework_pdc import HomeworkCreate
from schemas.student_pdc import IdType
from service.CONSTANTS import day_id_to_weekday
from service.student import StudentService


class HomeworkService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_homework_date(self, my_class_id: int, homework_date: date):
        homeworks = (
            self.session.query(Homework)
            .join(Schedule)
            .join(Class)
            .filter(Class.id == my_class_id, Homework.date == homework_date)
            .all()
        )
        return homeworks

    def create_homework(self, my_class_id: int, homework_raw_data: HomeworkCreate):
        homework_data = homework_raw_data.dict(exclude_unset=True, exclude={"photo_tg_id"})
        if homework_data["date"] == "auto":
            homework_data["date"] = Schedule.get_date_next_lesson(self.session, my_class_id, homework_data["lesson"])
            if homework_data["date"] is None:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="The automatic date did not find the lesson",
                    err_id=my_err.HOMEWORK_NO_SUCH_LESSON,
                )

        homework_data["schedule_id"] = (
            self.session.query(Schedule.id)
            .join(Lesson)
            .join(Class)
            .filter(Lesson.name == homework_data["lesson"], Class.id == my_class_id)
            .first()
        )
        del homework_data["lesson"]
        if homework_data["schedule_id"] is None:
            raise APIError(
                status_code=status.HTTP_404_NOT_FOUND, msg="Schedule not found", err_id=my_err.HOMEWORK_NO_SUCH_LESSON
            )
        homework_data["schedule_id"] = homework_data["schedule_id"][0]
        homework_data["author_id"] = self.session.query(Student).filter(Student.tg_id == homework_data['author_tg_id']).first().id
        del homework_data['author_tg_id']

        homework = Homework(**homework_data)
        self.session.add(homework)
        self.session.flush()

        homework_data = homework_raw_data.dict(exclude_unset=True, include={"photo_tg_id"})
        if "photo_tg_id" in homework_data:
            for photo_id in homework_data["photo_tg_id"]:
                self.session.add(TgPhoto(homework_id=homework.id, photo_id=photo_id))
        self.session.commit()
        return homework