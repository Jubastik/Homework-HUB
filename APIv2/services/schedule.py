from fastapi import Depends
from sqlalchemy.orm import Session
from starlette import status

import my_err
from database.db_session import get_session
from database.schedules import Schedule
from database.week_days import WeekDay
from my_err import APIError


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
