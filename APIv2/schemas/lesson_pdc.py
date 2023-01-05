from pydantic import BaseModel


class LessonReturn(BaseModel):
    name: str

    class Config:
        orm_mode = True
