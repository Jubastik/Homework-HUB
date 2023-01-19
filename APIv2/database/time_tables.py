import sqlalchemy

from .db_session import SqlAlchemyBase


class TimeTable(SqlAlchemyBase):
    __tablename__ = "time_tables"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    class_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("classes.id"), nullable=False)
    number_of_lesson = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    begin_time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    end_time = sqlalchemy.Column(sqlalchemy.Time, nullable=False)
    __table_args__ = (sqlalchemy.UniqueConstraint("class_id", "number_of_lesson"),)

    def __repr__(self):
        return f"<TimeTable> {self.id} {self.number_of_lesson} {self.begin_time} {self.end_time}"
