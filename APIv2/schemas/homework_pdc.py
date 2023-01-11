from datetime import date
from typing import Literal

from pydantic import BaseModel, root_validator
from starlette import status

import my_err
from my_err import APIError
from schemas.schedule_pdc import ScheduleReturn

from APIv2.schemas.student_pdc import StudentReturn


class TgPhoto(BaseModel):
    photo_id: str

    class Config:
        orm_mode = True


class HomeworkBase(BaseModel):
    pass


class HomeworkCreate(HomeworkBase):
    author_tg_id: int
    lesson: str
    text_homework: str | None
    date: date | Literal["auto"]
    photo_tg_id: list[int] | None

    @root_validator
    def correctness_check(cls, values):
        if values["text_homework"] is None and values["photo_tg_id"] is None:
            raise APIError(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                msg="The request must contain a photo id or text",
                err_id=my_err.VALIDATION_ERROR,
            )
        return values


class HomeworkReturn(HomeworkBase):
    date: date
    schedule: ScheduleReturn
    text_homework: str | None
    photo_tg_id: list[TgPhoto] | None
    author: StudentReturn

    class Config:
        orm_mode = True
