import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Chat(SqlAlchemyBase, SerializerMixin):
    __tablename__ = "Chats"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=False)
    class_id = sqlalchemy.Column(
        sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id")
    )
    my_class = orm.relationship("Class", back_populates="chats")

    def __repr__(self):
        return f"<Group> {self.id} {self.class_id}"
