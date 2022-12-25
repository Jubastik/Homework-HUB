from enum import Enum

from fastapi import Depends, HTTPException

from schemas.student_pdc import IdType
from services.student import StudentService


def process_id(student_id: int, id_type: IdType, service: StudentService = Depends()):
    return service.convert_id(id_type, student_id)


def optional_process_id(student_id: int | None = None, id_type: IdType | None = None, service: StudentService = Depends()):
    if student_id is not None and id_type is not None:
        return service.convert_id(id_type, student_id)
    if student_id != id_type:
        raise HTTPException(status_code=400, detail="You must specify both id and id_type or none of them")
    return None
