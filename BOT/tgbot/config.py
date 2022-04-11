import configparser
from dataclasses import dataclass


@dataclass
class TgBot:
    token: str
    use_redis: bool


@dataclass
class Config:
    tg_bot: TgBot


def cast_bool(value: str) -> bool:
    if not value:
        return False
    return value.lower() in ("true", "t", "1", "yes")


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    tg_bot = config["tg_bot"]

    return Config(
        tg_bot=TgBot(
            token=tg_bot["token"],
            use_redis=cast_bool(tg_bot.get("use_redis")),
        ),
    )
