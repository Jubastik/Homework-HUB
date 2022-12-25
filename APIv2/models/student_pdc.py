from pydantic import BaseModel


class StudentPDC(BaseModel):
    name: int
    is_admin: bool
    is_superuser: bool

    class Config:
        orm_mode = True
