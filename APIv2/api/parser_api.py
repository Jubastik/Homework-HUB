import datetime
from typing import List

from fastapi import APIRouter, Depends, Response
from starlette import status

import my_err
from api.dependencies import process_user_id
from my_err import APIError
from schemas.parser_pdc import ParserReturn, ParserCreate, ParserHomeworkReturn
from service.parser import ParserService
from service.redis_methods import get_cache, set_cache, del_cache, get_cache_time

router = APIRouter(
    prefix="/parser",
    tags=["parser"],
)


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
        cache_data = [ParserReturn.from_orm(d).dict(exclude_unset=True) for d in data]
        set_cache(f"cp_{obj_id}", cache_data, 3 * 60)
    else:
        data = [ParserReturn(**d) for d in data]
    return data


@router.post("/", response_model=ParserReturn)
async def create_parser(
    parser: ParserCreate, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Создать парсер
    """
    del_cache(f"cp_{obj_id}")
    return service.create_parser(obj_id, parser)


@router.get("/homework/{hwdate}", response_model=ParserHomeworkReturn)
async def get_pars_homework(
    hwdate: datetime.date, obj_id: int = Depends(process_user_id), service: ParserService = Depends()
):
    """
    Получить домашку с помощью парсера
    """

    def _get(obj_id: int, hwdate: datetime.date):
        return service.get_pars_homework(obj_id, hwdate)

    id_student_with_parser = service.get_user_with_ed(obj_id)

    cache_ttl = get_cache_time(f"hw_{id_student_with_parser}_{hwdate}")

    if cache_ttl is None or cache_ttl < (60 * 60 * 60) - (2 * 60 * 60):
        try:
            data = _get(id_student_with_parser, hwdate)
            cache_data = data.dict(exclude_unset=True)
            if "mailing_time" in cache_data["author"] and cache_data["author"]["mailing_time"] is not None:
                cache_data["author"]["mailing_time"] = str(cache_data["author"]["mailing_time"])
            set_cache(f"hw_{obj_id}_{hwdate}", cache_data, 60 * 60 * 60)
            return data
        except APIError as e:
            if e.err_id == my_err.ParserAccessError:
                data = get_cache(f"hw_{id_student_with_parser}_{hwdate}")
                if data is None:
                    raise e
                data["homework"].insert(
                    0,
                    {
                        "subject": "Ошибка ЭД",
                        "date": "01.01.2023",
                        "text": "Дневник недоступен. Отправлено последнее сохраненное дз",
                    },
                )
                data = ParserHomeworkReturn(**data)
                return data
            raise e
    else:
        data = get_cache(f"hw_{id_student_with_parser}_{hwdate}")
        data = ParserHomeworkReturn(**data)
        return data


@router.delete("/")
async def del_pars(obj_id: int = Depends(process_user_id), parser_type=1, service: ParserService = Depends()):
    """
    Удаление парсера
    """
    service.delete_parser(obj_id, parser_type)
    del_cache(f"cp_{obj_id}")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
