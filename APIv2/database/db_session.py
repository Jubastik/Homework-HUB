import os

import sqlalchemy as sa
import sqlalchemy.ext.declarative as dec
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
from settings import settings

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    db_engine = settings().DB_ENGINE
    if db_engine == "postgresql":
        db_connection = f"postgresql://{settings().POSTGRESQL_USERNAME}:{settings().POSTGRESQL_PASSWORD}@{settings().POSTGRESQL_HOST}:{settings().POSTGRESQL_PORT}/{settings().POSTGRESQL_DB_NAME}"
    elif db_engine == "sqlite":
        db_dir = settings().SQLITE_DIR
        db_connection = f"sqlite:///{db_dir.strip()}?check_same_thread=False"
    else:
        raise Exception("Неподдерживаемый тип базы данных.")

    print(f"Подключение к базе данных по адресу {db_connection}")

    engine = sa.create_engine(db_connection, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
