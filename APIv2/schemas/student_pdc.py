from datetime import time
from enum import Enum

from pydantic import BaseModel


class IdType(Enum):
    telegram = "student_tg"
    database = "student_db"


class StudentBase(BaseModel):
    name: str | None
    tg_id: int | None
    class_id: int | None
    is_admin: bool | None
    is_superuser: bool | None
    mailing_time: time | None
    mailing_stopped: bool | None


class StudentCreate(StudentBase):
    name: str
    class_token: int | None


class StudentUpdate(StudentBase):
    pass


class StudentReturn(StudentBase):
    id: int

    class Config:
        orm_mode = True
