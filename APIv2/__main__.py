import uvicorn

from database import db_session
from settings import settings

db_session.global_init()
uvicorn.run(
    "APIv2.app:app",
    reload=True,
    host=settings().API_HOST,
    port=settings().API_PORT,
)