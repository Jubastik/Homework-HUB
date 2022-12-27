import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.sql import func

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase):
    __tablename__ = "students"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    my_class = orm.relationship("Class", back_populates="student")
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_superuser = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    homeworks = orm.relationship("Homework", cascade="all, delete-orphan")
    # Mailings
    mailing_time = sqlalchemy.Column(
        sqlalchemy.Time, server_default=func.time(17, 0, 0), default=datetime.time(17, 0, 0)
    )
    mailing_stopped = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f"<Student> {self.id} {self.name} {self.my_class} {self.is_admin}"
