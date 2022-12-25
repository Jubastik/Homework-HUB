import datetime

import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase):
    __tablename__ = "Chats"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.BigInteger, unique=True, nullable=False)
    class_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id")
    )
    my_class = orm.relationship("Class", back_populates="chats")

    def __repr__(self):
        return f"<Group> {self.id} {self.class_id}"
