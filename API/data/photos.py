import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Photo(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'photos'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    homework_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('homeworks.id'))
    photo_dir = sqlalchemy.Column(sqlalchemy.String)
