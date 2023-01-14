from pydantic import BaseModel


class WeekDayReturn(BaseModel):
    name: str

    class Config:
        orm_mode = True
