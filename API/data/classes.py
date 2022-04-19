import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Class(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'classes'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String)
    class_token = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    vk_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    student = orm.relationship("Student", back_populates="my_class")
    schedules = orm.relationship("Schedule", back_populates="my_class")

    def __repr__(self):
        return f'<Class> {self.id} {self.name} {self.vk_id}'
