import uvicorn
from settings import settings

uvicorn.run(
    "APIv2.app:app",
    reload=True,
    host=settings().API_HOST,
    port=settings().API_PORT,
)
