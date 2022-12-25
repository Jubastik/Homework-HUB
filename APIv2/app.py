from fastapi import FastAPI
from api import router
from database import db_session

db_session.global_init()
app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {"message": "Hello HomeV2!"}
