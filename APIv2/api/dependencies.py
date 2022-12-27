from fastapi import Depends, status

import my_err
from my_err import APIError
from schemas.student_pdc import IdType
from services.student import StudentService


def process_id(obj_id: int, id_type: IdType, service: StudentService = Depends()):
    return service.convert_id(id_type, obj_id)


def optional_process_id(obj_id: int | None = None, id_type: IdType | None = None, service: StudentService = Depends()):
    if obj_id is not None and id_type is not None:
        return service.convert_id(id_type, obj_id)
    if obj_id != id_type:
        raise APIError(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="obj_id and id_type must be specified together",
            err_id=my_err.VALIDATION_ERROR,
        )
    return None
