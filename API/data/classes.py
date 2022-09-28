import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "classes"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    class_token = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    student = orm.relationship("Student", back_populates="my_class", cascade="all, delete-orphan")
    chats = orm.relationship("Chat", cascade="all, delete-orphan")
    schedules = orm.relationship("Schedule", back_populates="my_class", cascade="all, delete-orphan")
    time_tables = orm.relationship("TimeTable", cascade="all, delete-orphan")
    bans = orm.relationship("Ban_list", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Class> {self.id} {self.name} {self.vk_id}"
