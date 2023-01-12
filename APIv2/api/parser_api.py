import datetime
from typing import List, Literal

from fastapi import APIRouter, Depends

from api.dependencies import process_user_id
from schemas.homework_pdc import HomeworkReturn, HomeworkCreate
from schemas.parser_pdc import ParserReturn, ParserCreate, ParserHomeworkReturn
from service.homework import HomeworkService
from datetime import date

from service.parser import ParserService

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)


@router.get("/", response_model=List[ParserReturn])
async def clarify_parsers(obj_id: int = Depends(process_user_id), service: ParserService = Depends()):
    """
    Актуализировать информацию о состоянии парсеров юзера
    """
    return service.clarify_parsers(obj_id)


@router.post("/", response_model=ParserReturn)
async def create_parser(
    parser: ParserCreate, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Создать парсер
    """
    return service.create_parser(obj_id, parser)


@router.get("/homework/{date}", response_model=List[ParserHomeworkReturn])
async def get_pars_homework(
    hwdate: datetime.date, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Получить домашку с помощью парсера
    """
    return service.get_pars_homework(obj_id, hwdate)
