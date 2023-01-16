from fastapi import Depends, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

import my_err
from database.ban_list import Ban_list
from database.classes import Class
from database.db_session import get_session
from database.students import Student
from my_err import APIError
from schemas.student_pdc import StudentReturn, IdType, StudentCreate


class StudentService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def convert_id(self, id_type: IdType, id: int):
        if id_type == IdType.telegram:
            cur = self.session.query(Student).filter(Student.tg_id == id).first()
            if cur:
                return cur.id
        elif id_type == IdType.database:
            cur = self.session.query(Student).filter(Student.id == id).first()
            if cur:
                return id
        raise APIError(status_code=status.HTTP_404_NOT_FOUND, msg="Student not found", err_id=my_err.STUDENT_NOT_FOUND)

    def convert_class_token(self, class_token: str) -> int:
        class_id = self.session.query(Class.id).filter(Class.class_token == class_token).first()
        if not class_id:
            raise APIError(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Invalid class token", err_id=my_err.INVALID_CLASS_TOKEN
            )
        return class_id[0]

    def _get(self, student_id: int) -> Student:
        return self.session.query(Student).filter(Student.id == student_id).first()

    def check_ban_by_tg_id(self, tg_id: int, class_id: int) -> bool:
        return (
                self.session.query(Ban_list).filter(Ban_list.tg_id == tg_id, Ban_list.class_id == class_id).first() is not None
        )

    def get_student(self, student_id: int) -> Student:
        return self._get(student_id)

    def get_students(self) -> list[StudentReturn]:
        return self.session.query(Student).all()

    def get_students_in_my_class(self, student_id: int) -> list[Student]:
        student = self._get(student_id)
        if not student.class_id:
            raise APIError(
                status_code=status.HTTP_400_BAD_REQUEST,
                msg="You are not in a class",
                err_id=my_err.STUDENT_NOT_IN_CLASS,
            )
        return student.my_class.student

    def create_student(self, student: StudentCreate) -> Student:
        data = student.dict(exclude_unset=True)
        if "tg_id" in data:
            user = self.session.query(Student).filter(Student.tg_id == data["tg_id"]).first()
            if user:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="User with this telegram id already exists",
                    err_id=my_err.STUDENT_ALREADY_EXISTS,
                )
        if "class_token" in data:
            data["class_id"] = self.convert_class_token(data["class_token"])
            del data["class_token"]
        if "class_id" in data:
            my_class = self.session.query(Class).filter(Class.id == data["class_id"]).first()
            if not my_class:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="Invalid class id",
                    err_id=my_err.CLASS_NOT_FOUND,
                )
            if "tg_id" in data and self.check_ban_by_tg_id(data["tg_id"], data["class_id"]):
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg="You are banned from this class",
                    err_id=my_err.STUDENT_BAN_IN_CLASS,
                )
        new_student = Student(**data)
        self.session.add(new_student)
        try:
            self.session.commit()
        except IntegrityError:
            raise APIError(
                status_code=status.HTTP_400_BAD_REQUEST, msg="Invalid data", err_id=my_err.STUDENT_INIT_INVALID_DATA
            )
        return new_student

    def update_student(self, student_id: int, student: StudentCreate) -> Student:
        new_student = self._get(student_id)
        for field, value in student.dict(exclude_unset=True).items():
            try:
                if field == "class_id":
                    value = self.session.query(Class).filter(Class.id == value).first().id
                setattr(new_student, field, value)
            except Exception:
                raise APIError(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    msg=f"Invalid data. Field {field}, value {value}",
                    err_id=my_err.CLASS_NOT_FOUND,
                )
        self.session.commit()
        return new_student

    def delete_student(self, student_id: int) -> Student:
        student = self._get(student_id)
        self.session.delete(student)
        self.session.commit()
        return student
