from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

from api.dependencies import process_user_id, process_class_id
from schemas.ban_list_pdc import BanListReturn, BanListUserReturn
from schemas.student_pdc import IdType
from services.ban_list import BanListService

router = APIRouter(
    prefix="/ban",
    tags=["ban"],
)


@router.get("/{obj_id}", response_model=List[BanListReturn])
async def where_i_banned(obj_id: int, id_type: IdType, service: BanListService = Depends()):
    """
    Получить классы, где заблокирован пользователь
    """
    return service.get_ban_list(obj_id, id_type)


@router.get("/class/{obj_id}", response_model=List[BanListUserReturn])
async def get_class_ban_list(obj_id=Depends(process_class_id), service: BanListService = Depends()):
    """
    Получить список заблокированных пользователей в классе
    """
    return service.get_class_ban_list(obj_id)


@router.patch("/{obj_id}", response_model=BanListUserReturn)
async def ban_student(obj_id: int = Depends(process_user_id), service: BanListService = Depends()):
    """
    Заблокировать ученика в текущем классе
    """
    return service.ban_student(obj_id)


@router.delete("/{obj_id}")
async def unban_student(obj_id: int, id_type: IdType, class_id: int, service: BanListService = Depends()):
    """
    Разблокировать ученика в классе
    """
    service.unban_student(obj_id, id_type, class_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
