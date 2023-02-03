import json

import redis

from settings import settings

redis_con = None


def init_redis():
    global redis_con
    if settings().USE_REDIS:
        try:
            print("Подключение к Redis...")
            redis_con = redis.Redis(
                host=settings().REDIS_HOST, port=settings().REDIS_PORT, db=0, password=settings().REDIS_PASSWORD
            )
            print(redis_con.ping())
        except redis.exceptions.ConnectionError as e:
            print("Ошибка подключения к Redis:", e)
            exit(1)


def get_cache(key):
    if settings().USE_REDIS:
        if redis_con.exists(f"API_{key}"):
            return json.loads(redis_con.get(f"API_{key}"))
        return None
    else:
        return None


def get_cache_time(key):
    if settings().USE_REDIS:
        print(redis_con.ttl(f"API_{key}"))
        if redis_con.ttl(f"API_{key}") > 0:
            return redis_con.ttl(f"API_{key}")
        return None
    else:
        return None


def set_cache(key, value, expire=10) -> bool:
    if settings().USE_REDIS:
        redis_con.set(f"API_{key}", json.dumps(value), ex=expire)
        return True
    else:
        return False


def del_cache(key):
    if settings().USE_REDIS:
        redis_con.delete(f"API_{key}")
        return True
    else:
        return False
