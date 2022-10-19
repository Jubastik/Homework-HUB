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
    mailing_time = sqlalchemy.Column(sqlalchemy.Time, nullable=False, default="17:00")

    def __repr__(self):
        return f"<Group> {self.id} {self.class_id}"
