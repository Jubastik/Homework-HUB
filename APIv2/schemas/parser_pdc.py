from pydantic import BaseModel

from schemas.student_pdc import StudentReturn


class ParserReturn(BaseModel):
    platform_id: int
    active: bool

    class Config:
        orm_mode = True


class ParserCreate(BaseModel):
    platform_id: int
    login: str
    password: str


class ParserHomeworkInfoReturn(BaseModel):
    subject: str
    date: str
    text: str


class ParserHomeworkReturn(BaseModel):
    author: StudentReturn
    homework: list[ParserHomeworkInfoReturn]
