import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class TgPhoto(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "tg_photos"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    homework_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("homeworks.id")
    )
    photo_id = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"<Lesson> {self.id} {self.name}"
