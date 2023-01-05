import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


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
        return f"<Schedule> {self.id} {self.day.name} {self.slot.number_of_lesson} {self.lesson.name}"
