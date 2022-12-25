from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.db_session import get_session
from database.students import Student
from models.student_pdc import StudentPDC

router = APIRouter(
    prefix="/students",
)


@router.get("/", response_model=List[StudentPDC])
async def get_students(session: Session = Depends(get_session)):
    students = session.query(Student).all()
    return students
