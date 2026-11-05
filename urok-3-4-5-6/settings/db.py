from dataclasses import dataclass
from environs import Env


@dataclass
class DbConfig:
    url: str

    @staticmethod
    def from_env(env: Env) -> "DbConfig":
        return DbConfig(
            url=env.str('DB_URL')
        )