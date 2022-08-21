# HomeBot


**[Бот](https://t.me/hw_assistant_bot)** для сохранения и обмена домашним заданием  
**[Телеграм канал бота](https://t.me/hw_assistant)**

### Возможности бота
* Можно **сохранять** домашку в виде текста или картинки
* Можно **обмениваться** домашку с одноклассниками
* Можно **добавить бота в беседу** и делиться домашкой с незарегестрированными пользователями
___
### О проекте
Бот написан на базе библиотек [aiogram](https://pypi.org/project/aiogram/) и [Flask](https://pypi.org/project/Flask/)
Архитектура бота ориентируется на концепцию _REST_ и состоит из двух подпроектов:
* API - сервер, с базой данных и обработчиком запросов к ней
* BOT - телеграм бот, отвечающий за взаимодействие с юзером
___
### .env конфигурация
Для работы проекта необходимо заполнить два **.env** файла
Пустая конфигурация есть в **.env.example** файла

##### API/.env
```
API_DEBUG=True
API_HOST=""
API_PORT=8000
ROOT_TOKEN=""

DB_ENGINE = ""  # sqlite / postgresql

POSTGRESQL_USERNAME = ""
POSTGRESQL_PASSWORD = ""
POSTGRESQL_HOST = ""
POSTGRESQL_PORT = ""
POSTGRESQL_DB_NAME = ""

SQLITE_DIR = 'db/API.db'
```
| Параметр   |         Справка         |  Ожидаемое значение  |
| ---------- | :---------------------: | :------------------: |
| API_DEBUG  |      Режим дебага       |     True / False     |
| API_HOST   |          Хост           |         int          |
| API_PORT   |          Порт           |         int          |
| ROOT_TOKEN | Секретный ключ сервера* |         str          |
| DB_ENGINE  |         Вид БД          | sqlite / postgresql* |

*Должно **совпадать** с конфигурацией в BOT

##### BOT/.env
```
TG_TOKEN=""
API_SERVER=""
API_TOKEN=""
VERSION="server" # "local" / "server"
TG_ADMIN_CHAT=""
TG_OFFICAL_CHANNEL_ID=""
```
| Параметр              |         Справка         | Ожидаемое значение |
| --------------------- | :---------------------: | :----------------: |
| TG_TOKEN              |       Токен бота        |        str         |
| API_SERVER            |        Адрес API        |        str         |
| API_TOKEN             | Секретный ключ сервера* |        str         |
| VERSION               |         Версия          |   local / server   |
| TG_ADMIN_CHAT         |   Чат администраторов   |        str         |
| TG_OFFICAL_CHANNEL_ID |   Телеграм канал бота   |        str         |
