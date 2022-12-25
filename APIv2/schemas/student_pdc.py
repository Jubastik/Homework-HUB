from enum import Enum

from pydantic import BaseModel


class IdType(Enum):
    telegram = "telegram"
    database = "database"


class StudentBase(BaseModel):
    name: str


class StudentCreate(StudentBase):
    tg_id: int | None
    class_id: int | None
    is_superuser: bool | None
    mailing_time: str | None
    mailing_stopped: bool | None


class StudentReturn(StudentBase):
    is_admin: bool | None
    is_superuser: bool
    tg_id: int | None

    class Config:
        orm_mode = True
