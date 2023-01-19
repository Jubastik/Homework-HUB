import redis

from settings import settings

redis_con = None


def init_redis():
    global redis_con
    if settings().USE_REDIS:
        try:
            print("Подключение к Redis...")
            redis_con = redis.Redis(host=settings().REDIS_HOST, port=settings().REDIS_PORT, password="tmp")
            print(redis_con.ping())
        except redis.exceptions.ConnectionError as e:
            print("Ошибка подключения к Redis:", e)
            exit(1)


def get_cache(key):
    if settings().USE_REDIS:
        return redis_con.get(key)
    else:
        return None


def set_cache(key, value, expire=10):
    if settings().USE_REDIS:
        redis_con.set(key, value, ex=expire)
    else:
        return None
