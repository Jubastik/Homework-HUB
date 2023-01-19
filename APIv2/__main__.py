import uvicorn
from uvicorn.config import LOGGING_CONFIG

from settings import settings

LOGGING_CONFIG["formatters"]["access"]["fmt"] = '%(asctime)s %(levelprefix)s %(client_addr)s - "%(request_line)s" %(status_code)s'
uvicorn.run(
    "app:app",
    reload=True,
    host=settings().API_HOST,
    port=settings().API_PORT,
)
