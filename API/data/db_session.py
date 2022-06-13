import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec
import os

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init():
    global __factory

    if __factory:
        return

    db_engine = os.getenv("DB_ENGINE", "sqlite")
    if db_engine == "postgresql":
        db_connection = f"postgresql://{os.getenv('POSTGRESQL_USERNAME')}:{os.getenv('POSTGRESQL_PASSWORD')}@{os.getenv('POSTGRESQL_HOST')}:{os.getenv('POSTGRESQL_PORT')}/{os.getenv('POSTGRESQL_DB_NAME')}"
    elif db_engine == "":
        db_dir = os.getenv("SQLITE_DIR")
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
