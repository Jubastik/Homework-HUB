import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase):
    __tablename__ = "homeworks"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"), nullable=False
    )
    date = sqlalchemy.Column(sqlalchemy.Date, nullable=False)
    schedule_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("schedules.id"), nullable=False
    )
    schedule = orm.relationship("Schedule")
    text_homework = sqlalchemy.Column(sqlalchemy.String)
    photo_tg_id = orm.relationship("TgPhoto", cascade="all, delete-orphan")
    photo_dir = sqlalchemy.Column(sqlalchemy.String)
