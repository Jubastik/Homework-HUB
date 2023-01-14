import datetime

import sqlalchemy
from sqlalchemy import orm
from sqlalchemy.sql import func

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase):
    __tablename__ = "classes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    class_token = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    # Mailings
    mailing_time = sqlalchemy.Column(sqlalchemy.Time, server_default=func.time(17, 0, 0), default=datetime.time(17, 0, 0))
    mailing_stopped = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    # Relationships
    student = orm.relationship("Student", back_populates="my_class", cascade="all, delete-orphan")
    chats = orm.relationship("Chat", cascade="all, delete-orphan")
    schedules = orm.relationship("Schedule", back_populates="my_class", cascade="all, delete-orphan")
    time_tables = orm.relationship("TimeTable", cascade="all, delete-orphan")
    bans = orm.relationship("Ban_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Class> {self.id} {self.name} {self.vk_id}"
