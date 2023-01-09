import datetime

from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.classes import Class
from database.db_session import get_session
from database.schedules import Schedule
from database.students import Student
from database.time_tables import TimeTable
from database.week_days import WeekDay
from my_err import APIError
from schemas.schedule_pdc import ScheduleCurrentReturn
from services.CONSTANTS import day_id_to_weekday


class ScheduleService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all_schedules(self, class_id: int):
        return self.session.query(Schedule).filter(Schedule.class_id == class_id).all()

    def get_schedule(self, class_id: int, day: str):
        schedule = (
            self.session.query(Schedule)
            .filter(Schedule.class_id == class_id)
            .join(WeekDay)
            .filter(WeekDay.name == day)
            .all()
        )
        return schedule

    def get_current_schedule(self, class_id: int):
        # __now = datetime.datetime(2021, 9, 1, 10, 30)
        start_lesson = (datetime.datetime.now() + datetime.timedelta(minutes=10)).time()
        day = day_id_to_weekday[datetime.datetime.today().weekday()]

        now_lessons = (
            self.session.query(Schedule)
            .join(WeekDay)
            .join(TimeTable)
            .join(Class)
            .filter(
                Class.id == class_id,
                WeekDay.name == day,
                TimeTable.begin_time < start_lesson,
            )
            .order_by(TimeTable.begin_time)
            .all()
        )[-2::]
        data = []
        for lesson in now_lessons:
            d = ScheduleCurrentReturn(lesson=lesson.lesson, day=lesson.day, slot=lesson.slot)
            d.lesson_date = Schedule.get_date_next_lesson(self.session, class_id, lesson.lesson.name)
            data.append(d)
        return data
