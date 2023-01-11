from typing import List

from fastapi import APIRouter, Depends, Response

from api.dependencies import process_user_id, optional_process_user_id, process_class_id
from schemas.class_pdc import MyClassReturn, MyClassCreate, MyClassUpdate
from service.my_class import MyClassService

router = APIRouter(
    prefix="/class",
    tags=["class"],
)


@router.get("/", response_model=List[MyClassReturn])
async def get_classes(service: MyClassService = Depends()):
    """
    Получить все классы
    """
    return service.get_all_classes()


@router.get("/{obj_id}", response_model=MyClassReturn)
async def get_class(obj_id: int = Depends(process_class_id), service: MyClassService = Depends()):
    """
    Получить класс по id
    """
    return service.get_class(obj_id)


@router.post("/", response_model=MyClassReturn)
async def create_class(
    my_class: MyClassCreate, obj_id: int = Depends(process_user_id), service: MyClassService = Depends()
):
    """
    Создать класс
    """
    return service.create_class(obj_id, my_class)


@router.patch("/{obj_id}", response_model=MyClassReturn)
async def update_class(
    my_class: MyClassUpdate, obj_id: int = Depends(process_class_id), service: MyClassService = Depends()
):
    """
    Обновить класс
    """
    return service.update_class(obj_id, my_class)


#
#
# @router.delete("/{obj_id}")
# async def delete_student(obj_id: int = Depends(process_id), service: StudentService = Depends()):
#     """
#     Удалить ученика
#     """
#     service.delete_student(obj_id)
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
