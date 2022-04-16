import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Homework(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'homeworks'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    author_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"))
    date = sqlalchemy.Column(sqlalchemy.Date)
    schedule_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("schedules.id"))
    text_homework = sqlalchemy.Column(sqlalchemy.String)
