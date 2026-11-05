from dataclasses import dataclass
from environs import Env

from .db import DbConfig
from .bot import BotConfig

@dataclass
class Config:
    db: DbConfig
    bot: BotConfig


def load_config(env_path: str | None = None):
    env = Env()
    env.read_env(env_path)

    return Config(
        db=DbConfig.from_env(env),
        bot=BotConfig.from_env(env)
    )


config = load_config()
