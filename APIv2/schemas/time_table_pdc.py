from datetime import time

from pydantic import BaseModel, Field


class TimeTableCreate(BaseModel):
    number_of_lesson: int = Field(alias="lesson_number")
    begin_time: time
    end_time: time

