from typing import List, Literal

from fastapi import APIRouter, Depends

from api.dependencies import process_class_id
from schemas.schedule_pdc import ScheduleReturn
from services.schedule import ScheduleService

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
