from fastapi import Depends
from sqlalchemy.orm import Session

import my_err
from database.ban_list import Ban_list
from database.db_session import get_session
from database.students import Student
from my_err import APIError
from schemas.student_pdc import IdType


class BanListService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_ban_list(self, student_id: int, id_type: IdType):
        if id_type == IdType.telegram:
            return self.session.query(Ban_list).filter(Ban_list.tg_id == student_id).all()
        raise APIError(422, my_err.IN_DEVELOPMENT, "Неверный тип id")

    def get_class_ban_list(self, class_id: int):
        return self.session.query(Ban_list).filter(Ban_list.class_id == class_id).all()

    def ban_student(self, student_id: int):
        student = self.session.query(Student).filter(Student.id == student_id).first()
        if student is None:
            raise APIError(404, my_err.STUDENT_NOT_FOUND, "Пользователь не был найден.")
        ban = Ban_list(tg_id=student.tg_id, class_id=student.class_id, name=student.name)
        self.session.add(ban)
        self.session.delete(student)
        self.session.commit()
        return ban

    def unban_student(self, ban_id):
        ban = self.session.query(Ban_list).filter(Ban_list.id == ban_id).first()
        if ban is None:
            raise APIError(404, my_err.STUDENT_NOT_FOUND, "Пользователь не был найден.")
        self.session.delete(ban)
        self.session.commit()
