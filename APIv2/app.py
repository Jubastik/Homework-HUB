import logging
from urllib.request import Request
import redis

import sentry_sdk
from fastapi import FastAPI, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from sentry_sdk.integrations.logging import LoggingIntegration
from starlette import status
from starlette.responses import JSONResponse

import my_err
from api import router
from api.dependencies import verify_root_token
from database import db_session
from settings import settings

if settings().SENTRY_DSN is not None and settings().SENTRY_DSN != "":
    sentry_sdk.init(
        dsn=settings().SENTRY_DSN,
        traces_sample_rate=1.0
    )

tags_metadata = [
    {
        "name": "student",
        "description": "Взаимодействие с учениками",
    }
]

if settings().USE_REDIS:
    try:
        print("Подключение к Redis...")
        redis_con = redis.Redis(host=settings().REDIS_HOST, port=settings().REDIS_PORT, password='tmp')
        print(redis_con.ping())
    except redis.exceptions.ConnectionError as e:
        print("Ошибка подключения к Redis:", e)
        exit(1)

db_session.global_init()
app = FastAPI(
    title="APIv2",
    description="Обновлённое API для Homework HUB",
    openapi_tags=tags_metadata,
    dependencies=[Depends(verify_root_token)],
    debug=settings().API_DEBUG,
)
app.include_router(router)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content=jsonable_encoder({"detail": exc.errors(), "ErrorID": my_err.VALIDATION_ERROR}),
    )


@app.exception_handler(my_err.APIError)
async def api_error_handler(request: Request, exc: my_err.APIError):
    # print(exc)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": [{"msg": exc.msg}], "ErrorID": exc.err_id},
    )


@app.exception_handler(500)
async def internal_server_error_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": [{"msg": "Internal server error"}], "ErrorID": my_err.INTERNAL_SERVER_ERROR},
    )


@app.get("/")
async def root():
    return {"message": "Hello HomeV2!"}
