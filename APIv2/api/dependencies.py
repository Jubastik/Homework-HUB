from fastapi import Depends, status

import my_err
from my_err import APIError
from schemas.class_pdc import ExtendedIdType
from schemas.student_pdc import IdType
from services.ban_list import BanListService
from services.my_class import MyClassService
from services.student import StudentService
from settings import settings


def verify_root_token(root_token: str):
    if root_token != settings().ROOT_TOKEN:
        raise APIError(
            status_code=status.HTTP_401_UNAUTHORIZED,
            msg="Invalid root token",
            err_id=my_err.INVALID_ROOT_TOKEN,
        )


def process_user_id(obj_id: int, id_type: IdType, service: StudentService = Depends()):
    return service.convert_id(id_type, obj_id)


def process_banned_id(obj_id: int, id_type: IdType, service: BanListService = Depends()):
    return service.convert_id(id_type, obj_id)


def optional_process_user_id(
    obj_id: int | None = None, id_type: IdType | None = None, service: StudentService = Depends()
):
    if obj_id is not None and id_type is not None:
        return service.convert_id(id_type, obj_id)
    if obj_id != id_type:
        raise APIError(
            status_code=status.HTTP_400_BAD_REQUEST,
            msg="obj_id and id_type must be specified together",
            err_id=my_err.VALIDATION_ERROR,
        )
    return None


def process_class_id(obj_id: int, id_type: ExtendedIdType, service: MyClassService = Depends()):
    return service.convert_id(id_type, obj_id)
