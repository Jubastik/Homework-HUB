import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Ban_list(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Ban_list"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    class_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), nullable=False
    )

    def __repr__(self):
        return f"<Banned user> {self.id} {self.tg_id} {self.class_id}"