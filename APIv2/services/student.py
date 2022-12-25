from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from database.classes import Class
from database.db_session import get_session
from database.students import Student
from schemas.student_pdc import StudentReturn, IdType


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
        raise HTTPException(status_code=404, detail="Student not found")

    def get_student(self, student_id: int) -> StudentReturn:
        return self.session.query(Student).filter(Student.id == student_id).first()

    def get_students(self) -> list[StudentReturn]:
        return self.session.query(Student).all()

    def get_students_in_my_class(self, student_id: int) -> list[StudentReturn]:
        student = self.session.query(Student).filter(Student.id == student_id).first()
        return student.my_class.student

    # def create_student(self, student: StudentCreate):
    #     new_student = Student(
    #         tg_id=student.tg_id,
    #         name=student.name,
    #         is_admin=student.is_admin,
    #         is_superuser=student.is_superuser,
    #         my_class=student.my_class,
    #     )
    #     self.session.add(new_student)
    #     self.session.commit()
    #     return new_student
    #
    # def update_student(self, student_id: int, student: StudentCreate):
    #     db_student = self.session.query(Student).filter(Student.id == student_id).first()
    #     db_student.name = student.name
    #     db_student.is_admin = student.is_admin
    #     db_student.is_superuser = student.is_superuser
    #     db_student.my_class = student.my_class
    #     self.session.commit()
    #     return db_student
    #
    # def delete_student(self, student_id: int):
    #     db_student = self.session.query(Student).filter(Student.id == student_id).first()
    #     self.session.delete(db_student)
    #     self.session.commit()
    #     return db_student
    #
    # def get_student_by_tg_id(self, tg_id: int):
    #     return self.session.query(Student).filter(Student.tg_id == tg_id).first()
    #
    # def get_students_by_class_id(self, class_id: int):
    #     return self.session.query(Student).filter(Student.my_class == class_id).all()
