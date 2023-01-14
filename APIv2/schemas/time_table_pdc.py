from datetime import time

from pydantic import BaseModel, Field


class TimeTableBase(BaseModel):
    begin_time: time
    end_time: time


class TimeTableCreate(TimeTableBase):
    number_of_lesson: int = Field(alias="lesson_number")


class TimeTableReturn(TimeTableBase):
    number_of_lesson: int

    class Config:
        orm_mode = True
