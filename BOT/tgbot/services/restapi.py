# Функции запросов на rest api (использовать await!)
# Пока что просто затычки => фильтры работают через жопу, надо в коде указывать кем воспринимать юзеров

# Tasks:
# !1) Реализация используемых фильтрами is_student, is_admin, is_developer


async def add_user(tguser_id):
    pass


async def is_student(tguser_id):
    return False


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    pass


async def is_developer(tguser_id):
    pass
