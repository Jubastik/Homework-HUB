from datetime import time
from enum import Enum
from typing import Literal

from pydantic import BaseModel

from schemas.schedule_pdc import ScheduleCreate
from schemas.time_table_pdc import TimeTableCreate


class ExtendedIdType(str, Enum):
    telegram = "student_tg"
    database = "student_db"
    my_class = "my_class_db"


class MyClassBase(BaseModel):
    name: str


class MyClassCreate(MyClassBase):
    schedules: list[ScheduleCreate]
    time_tables: list[TimeTableCreate]


class MyClassUpdate(MyClassBase):
    name: str | None
    class_token: int | Literal["auto"] | None
    mailing_time: time | None
    mailing_stopped: bool | None


class MyClassReturn(MyClassBase):
    id: int
    class_token: int
    mailing_time: time
    mailing_stopped: bool

    class Config:
        orm_mode = True
