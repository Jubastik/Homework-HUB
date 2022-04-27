import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class WeekDay(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "week_days"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, unique=True)

    def __repr__(self):
        return f"<WeekDay> {self.id} {self.name}"
