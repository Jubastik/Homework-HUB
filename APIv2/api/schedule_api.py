from typing import List, Literal

from fastapi import APIRouter, Depends, Query

from api.dependencies import process_class_id
from schemas.schedule_pdc import ScheduleReturn, ScheduleLessonsReturn
from service.schedule import ScheduleService

router = APIRouter(
    prefix="/schedule",
    tags=["schedule"],
)


@router.get("/", response_model=List[ScheduleReturn])
async def get_schedules(obj_id: int = Depends(process_class_id), service: ScheduleService = Depends()):
    """
    Получить все расписание класса
    """
    return service.get_all_schedules(obj_id)


@router.get("/{day}", response_model=List[ScheduleReturn])
async def get_schedule(
    day: Literal["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"],
    obj_id: int = Depends(process_class_id),
    service: ScheduleService = Depends(),
):
    """
    Получить расписание класса на конкретный день
    """
    return service.get_schedule(obj_id, day)


@router.get("/current_schedule/{obj_id}", response_model=List[ScheduleReturn])
async def get_current_schedule(obj_id=Depends(process_class_id), service: ScheduleService = Depends()):
    """
    Получить сейчас идущий урок
    """
    return service.get_current_schedule(obj_id)


@router.get("/next_date/{obj_id}", response_model=List[ScheduleLessonsReturn])
async def get_next_date(
    lessons: list[str] = Query(), obj_id=Depends(process_class_id), service: ScheduleService = Depends()
):
    return service.get_next_date(obj_id, lessons)
