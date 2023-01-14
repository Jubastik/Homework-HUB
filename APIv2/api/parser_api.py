import datetime
from functools import wraps
from typing import List, Literal

from cachetools import cached, TTLCache
from fastapi import APIRouter, Depends, Response
from starlette import status

from api.dependencies import process_user_id
from schemas.homework_pdc import HomeworkReturn, HomeworkCreate
from schemas.parser_pdc import ParserReturn, ParserCreate, ParserHomeworkReturn

from service.parser import ParserService

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)

clar_cache = TTLCache(maxsize=100, ttl=15)


@router.get("/", response_model=List[ParserReturn])
async def clarify_parsers(obj_id: int = Depends(process_user_id), service: ParserService = Depends()):
    """
    Актуализировать информацию о состоянии парсеров юзера
    """

    @cached(cache=clar_cache)
    def _get(obj_id):
        return service.clarify_parsers(obj_id)

    return _get(obj_id)


@router.post("/", response_model=ParserReturn)
async def create_parser(
    parser: ParserCreate, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Создать парсер
    """
    return service.create_parser(obj_id, parser)


hw_cache = TTLCache(maxsize=500, ttl=600)


@router.get("/homework/{hwdate}", response_model=ParserHomeworkReturn)
async def get_pars_homework(
    hwdate: datetime.date, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Получить домашку с помощью парсера
    """

    @cached(cache=hw_cache)
    def _get(obj_id: int, hwdate: datetime.date):
        return service.get_pars_homework(obj_id, hwdate)

    return _get(obj_id, hwdate)


@router.delete("/")
async def del_pars(obj_id: int = Depends(process_user_id), parser_type=1, service: ParserService = Depends()):
    """
    Удаление парсера
    """
    service.delete_parser(obj_id, parser_type)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
