import datetime
import json
from typing import List

from cachetools import cached, TTLCache
from fastapi import APIRouter, Depends, Response
from starlette import status

from api.dependencies import process_user_id
from schemas.parser_pdc import ParserReturn, ParserCreate, ParserHomeworkReturn
from service.parser import ParserService
from service.redis_methods import get_cache, set_cache

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)

clar_cache = TTLCache(maxsize=100, ttl=45)


@router.get("/", response_model=List[ParserReturn])
async def clarify_parsers(obj_id: int = Depends(process_user_id), service: ParserService = Depends()):
    """
    Актуализировать информацию о состоянии парсеров юзера
    """

    def _get(obj_id):
        return service.clarify_parsers(obj_id)

    data = get_cache(f"cp_{obj_id}")
    if data is None:
        data = _get(obj_id)
        data = json.dumps([ParserReturn.from_orm(d).dict() for d in data])
        set_cache(f"cp_{obj_id}", data, 20)
    else:
        data = [ParserReturn(**d) for d in json.loads(data)]
    return data


@router.post("/", response_model=ParserReturn)
async def create_parser(
    parser: ParserCreate, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Создать парсер
    """
    return service.create_parser(obj_id, parser)


hw_cache = TTLCache(maxsize=500, ttl=60 * 60)


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

    id_student_with_parser = service.get_user_with_ed(obj_id)
    return _get(id_student_with_parser, hwdate)


@router.delete("/")
async def del_pars(obj_id: int = Depends(process_user_id), parser_type=1, service: ParserService = Depends()):
    """
    Удаление парсера
    """
    service.delete_parser(obj_id, parser_type)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
