import sqlalchemy

from database.db_session import SqlAlchemyBase


class Parser(SqlAlchemyBase):
    __tablename__ = "parsers"
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    student_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("students.id"), nullable=False)
    platform_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    active = sqlalchemy.Column(sqlalchemy.Boolean, nullable=False, default=True)
    x_jwt_token = sqlalchemy.Column(sqlalchemy.String, nullable=False)

    def __repr__(self):
        return f"<Parser> {self.id} {self.student_id} {self.active}"
