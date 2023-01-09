import datetime
from typing import Literal

from pydantic import BaseModel, Field

from schemas.lesson_pdc import LessonReturn
from schemas.time_table_pdc import TimeTableReturn
from schemas.week_days_pdc import WeekDayReturn


class ScheduleBase(BaseModel):
    pass


class ScheduleReturn(ScheduleBase):
    lesson: LessonReturn
    day: WeekDayReturn
    slot: TimeTableReturn

    class Config:
        orm_mode = True


class ScheduleCurrentReturn(ScheduleReturn):
    lesson_date: datetime.date | None


class ScheduleCreate(ScheduleBase):
    lesson: str
    day_of_week: Literal["понедельник", "вторник", "среда", "четверг", "пятница", "суббота"]
    lesson_number: int
