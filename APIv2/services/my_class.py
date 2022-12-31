from random import randint

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.classes import Class
from database.db_session import get_session
from database.lessons import Lesson
from database.schedules import Schedule
from database.students import Student
from database.time_tables import TimeTable
from my_err import APIError
from schemas.class_pdc import MyClassCreate


class MyClassService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def generate_class_token(self):
        token = randint(10000, 99999)
        while self.session.query(Class).filter(Class.class_token == token).first():
            token = randint(10000, 99999)
        return token

    def get_all_classes(self):
        return self.session.query(Class).all()

    def create_class(self, creator_id: int, my_class_data: MyClassCreate):
        """!!! продумать исключения!!!"""

        # Создание класса
        data = my_class_data.dict(exclude_unset=True, include={"name"})
        data["class_token"] = self.generate_class_token()
        my_class = Class(**data)
        self.session.add(my_class)
        self.session.flush()

        # Назначение админа
        admin = self.session.query(Student).filter(Student.id == creator_id).first()
        admin.is_admin = True
        admin.class_id = my_class.id
        self.session.flush()

        # Создание таймтейблов
        data = my_class_data.dict(exclude_unset=True, include={"time_tables"})
        for time_table in data["time_tables"]:
            time_table["class_id"] = my_class.id
            time_table = TimeTable(**time_table)
            self.session.add(time_table)
        self.session.flush()

        # Создание расписания
        data = my_class_data.dict(exclude_unset=True, include={"schedules"})
        for schedule in data["schedules"]:
            lesson = self.session.query(Lesson).filter(Lesson.name == schedule["lesson"]).first()
            if not lesson:
                lesson = Lesson(name=schedule["lesson"])
                self.session.add(lesson)
                self.session.flush()
            slot = self.session.query(TimeTable).filter(TimeTable.class_id == my_class.id,
                                                        TimeTable.number_of_lesson == schedule["lesson_number"]).first()
            if not slot:
                raise APIError(status_code=status.HTTP_400_BAD_REQUEST, err_id=my_err.SLOT_NOT_FOUND, msg="Invalid lesson number")

            schedule = Schedule(class_id=my_class.id, day_id=schedule["day_of_week"].value, slot_id=slot.id, lesson_id=lesson.id)
            self.session.add(schedule)
        self.session.commit()

        return my_class
