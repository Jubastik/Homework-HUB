import sqlalchemy
from sqlalchemy import orm
from sqlalchemy_serializer import SerializerMixin

from .db_session import SqlAlchemyBase


class Student(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'students'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    tg_id = sqlalchemy.Column(sqlalchemy.Integer, unique=True, nullable=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"))
    my_class = orm.relationship("Class", back_populates="student")
    name = sqlalchemy.Column(sqlalchemy.String)
    is_admin = sqlalchemy.Column(sqlalchemy.Boolean, default=False)
    is_superuser = sqlalchemy.Column(sqlalchemy.Boolean, default=False)

    def __repr__(self):
        return f'<Student> {self.id} {self.name} {self.my_class} {self.is_admin}'
