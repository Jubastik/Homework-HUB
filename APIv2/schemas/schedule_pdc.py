from enum import Enum

from pydantic import BaseModel, Field


class DayType(Enum):
    monday = 0
    tuesday = 1
    wednesday = 2
    thursday = 3
    friday = 4
    saturday = 5
    sunday = 6


class ScheduleCreate(BaseModel):
    lesson: str
    day_of_week: DayType
    lesson_number: int
