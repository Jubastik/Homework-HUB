# Функции запросов на rest api (использовать await!)
# Пока что просто затычки => фильтры работают через жопу, надо в коде указывать кем воспринимать юзеров

# Tasks:
# !1) Реализация используемых фильтрами is_student, is_admin, is_developer
# 2) add_user


async def is_student(tguser_id):
    return False


async def is_unregistered(tguser_id):
    return not (await is_student(tguser_id))


async def is_admin(tguser_id):
    pass


async def is_developer(tguser_id):
    pass


# Вообще по хорошему создать вспомогательный класс для homework, так будет удобней и красивше.
async def add_homework(tguser_id, homework: dict):
    pass


def register_user(tguser_id, classid):
    """Добавление юзера в бд, возвращает True если успешно, в противном случае False"""
    return True

def register_class(tguser_id, data):
    """Добавление юзера в бд, возвращает True если успешно, в противном случае False"""
    return True
