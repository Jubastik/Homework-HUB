from pydantic import BaseModel


class BanListReturn(BaseModel):
    class_id: int

    class Config:
        orm_mode = True


class BanListUserReturn(BaseModel):
    id: int
    tg_id: int
    name: str

    class Config:
        orm_mode = True
