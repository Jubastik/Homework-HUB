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
from database.week_days import WeekDay
from my_err import APIError
from schemas.class_pdc import MyClassCreate, ExtendedIdType, MyClassUpdate


class MyClassService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def convert_id(self, id_type: ExtendedIdType, obj_id):
        my_class_id = None
        if id_type == ExtendedIdType.my_class:
            my_class_id = self.session.query(Class.id).filter(Class.id == obj_id).first()
        elif id_type == ExtendedIdType.telegram:
            my_class_id = self.session.query(Class.id).join(Student).filter(Student.tg_id == obj_id).first()
        elif id_type == ExtendedIdType.database:
            my_class_id = self.session.query(Class.id).join(Student).filter(Student.id == obj_id).first()
        if my_class_id:
            return my_class_id[0]
        raise APIError(status_code=status.HTTP_404_NOT_FOUND, msg="Class not found", err_id=my_err.CLASS_NOT_FOUND)

    def generate_class_token(self):
        token = randint(10000, 99999)
        while self.session.query(Class).filter(Class.class_token == token).first():
            token = randint(10000, 99999)
        return token

    def get_class(self, class_id: int):
        return self.session.query(Class).filter(Class.id == class_id).first()

    def get_all_classes(self):
        return self.session.query(Class).all()

    def update_class(self, class_id: int, my_class_data: MyClassUpdate):
        new_my_class = self.get_class(class_id)
        for field, value in my_class_data.dict(exclude_unset=True).items():
            try:
                if field == "class_token" and value == "auto":
                    value = self.generate_class_token()
                setattr(new_my_class, field, value)
            except Exception:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg=f"Invalid data. Field {field}, value {value}",
                    err_id=my_err.UPDATE_CLASS_INVALID_DATA,
                )
        self.session.commit()
        return new_my_class

    # def delete_class(self, class_id: int):
    #     """TODO:!!! продумать исключения!!!"""
    #     my_class = self.get_class(class_id)
    #     self.session.delete(my_class)
    #     self.session.commit()

    def create_class(self, creator_id: int, my_class_data: MyClassCreate):
        """TODO:!!! продумать исключения!!!"""
        generate_week_days()

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
            slot = (
                self.session.query(TimeTable)
                .filter(TimeTable.class_id == my_class.id, TimeTable.number_of_lesson == schedule["lesson_number"])
                .first()
            )
            if not slot:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST, err_id=my_err.SLOT_NOT_FOUND, msg="Invalid lesson number"
                )
            schedule["day_of_week"] = self.session.query(WeekDay.id).filter(WeekDay.name == schedule["day_of_week"]).first()[0]
            schedule = Schedule(
                class_id=my_class.id, day_id=schedule["day_of_week"], slot_id=slot.id, lesson_id=lesson.id
            )
            self.session.add(schedule)
        self.session.commit()

        return my_class


def generate_week_days():
    session = next(get_session())
    if session.query(WeekDay).count() == 0:
        for day in ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]:
            session.add(WeekDay(name=day))
        session.commit()
    session.close()
