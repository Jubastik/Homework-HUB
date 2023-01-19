from datetime import date
from typing import List

from fastapi import APIRouter, Depends

from api.dependencies import process_class_id
from schemas.homework_pdc import HomeworkReturn, HomeworkCreate
from service.homework import HomeworkService

router = APIRouter(
    prefix="/homework",
    tags=["homework"],
)


@router.get("/{homework_date}", response_model=List[HomeworkReturn])
async def get_homeworks(
    homework_date: date, obj_id: int = Depends(process_class_id), service: HomeworkService = Depends()
):
    """
    Получить дз на дату
    """
    return service.get_homework_date(obj_id, homework_date)


@router.post("/", response_model=HomeworkReturn)
async def create_homework(
    homework: HomeworkCreate, obj_id: int = Depends(process_class_id), service: HomeworkService = Depends()
):
    """
    Создать дз
    """
    return service.create_homework(obj_id, homework)
