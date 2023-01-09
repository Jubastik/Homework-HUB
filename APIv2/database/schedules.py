import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.orm import Session

from .db_session import SqlAlchemyBase
from .lessons import Lesson
from .week_days import WeekDay


class Schedule(SqlAlchemyBase):
    __tablename__ = "schedules"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), nullable=False)
    my_class = orm.relationship("Class", back_populates="schedules")

    day_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("week_days.id"), nullable=False)
    day = orm.relationship("WeekDay")

    slot_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("time_tables.id"), nullable=False)
    slot = orm.relationship("TimeTable")

    lesson_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("lessons.id"), nullable=False)
    lesson = orm.relationship("Lesson")
    __table_args__ = (sqlalchemy.UniqueConstraint("class_id", "slot_id", "day_id"),)

    def __repr__(self):
        return f"<Schedule> {self.id} {self.day.name} {self.day_id} {self.slot.number_of_lesson} {self.lesson.name}"

    @classmethod
    def get_date_next_lesson(cls, session, my_class_id: int, lesson_name: str):
        schedules = (
            session.query(Schedule.day_id)
            .join(Lesson)
            .filter(Schedule.class_id == my_class_id, Lesson.name == lesson_name)
            .order_by(Schedule.day_id)
            .all()
        )
        days = [_[0] for _ in schedules]
        now = datetime.datetime.now().weekday() +  1
        for i in range(now, 8):
            if i in days:
                return datetime.date.today() + datetime.timedelta(days=i - now)
        for i in range(1, now):
            if i in days:
                return datetime.date.today() + datetime.timedelta(days=(7 - now) + i)
        return datetime.date.today() + datetime.timedelta(days=7)
