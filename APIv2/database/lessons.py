import sqlalchemy

from .db_session import SqlAlchemyBase


class Lesson(SqlAlchemyBase):
    __tablename__ = "lessons"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"<Lesson> {self.id} {self.name}"
