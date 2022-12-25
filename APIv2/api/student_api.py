from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import process_id, optional_process_id
from schemas.student_pdc import StudentReturn
from services.student import StudentService

router = APIRouter(
    prefix="/students",
)


@router.get("/", response_model=List[StudentReturn])
async def get_students(student_id: int = Depends(optional_process_id), service: StudentService = Depends()):
    if student_id is None:
        return service.get_students()
    else:
        return service.get_students_in_my_class(student_id)


@router.get("/{student_id}", response_model=StudentReturn)
async def get_student(student_id: int = Depends(process_id), service: StudentService = Depends()):
    return service.get_student(student_id)
