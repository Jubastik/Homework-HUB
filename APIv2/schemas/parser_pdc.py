from pydantic import BaseModel


class ParserReturn(BaseModel):
    platform_id: int
    active: bool

    class Config:
        orm_mode = True


class ParserCreate(BaseModel):
    platform_id: int
    login: str
    password: str


class ParserHomeworkReturn(BaseModel):
    subject: str
    date: str
    text: str

