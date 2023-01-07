from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

from api.dependencies import process_user_id, optional_process_user_id
from schemas.student_pdc import StudentReturn, StudentCreate, StudentUpdate
from services.student import StudentService

router = APIRouter(
    prefix="/student",
    tags=["student"],
)


@router.get("/", response_model=List[StudentReturn])
async def get_students(obj_id: int = Depends(optional_process_user_id), service: StudentService = Depends()):
    """
    Получить всех учеников

    - Для получения учеников из класса, в котором состоит ученик с указанным id, необходимо указать id и id_type
    """
    if obj_id is None:
        return service.get_students()
    else:
        return service.get_students_in_my_class(obj_id)


@router.get("/{obj_id}", response_model=StudentReturn)
async def get_student(obj_id: int = Depends(process_user_id), service: StudentService = Depends()):
    """
    Получить ученика по id
    """
    return service.get_student(obj_id)


@router.post("/", response_model=StudentReturn)
async def create_student(student: StudentCreate, service: StudentService = Depends()):
    """
    Создать ученика
    """
    return service.create_student(student)


@router.patch("/{obj_id}", response_model=StudentReturn)
async def update_student(
    student: StudentUpdate, obj_id: int = Depends(process_user_id), service: StudentService = Depends()
):
    """
    Обновить ученика
    """
    return service.update_student(obj_id, student)


@router.delete("/{obj_id}")
async def delete_student(obj_id: int = Depends(process_user_id), service: StudentService = Depends()):
    """
    Удалить ученика
    """
    service.delete_student(obj_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
