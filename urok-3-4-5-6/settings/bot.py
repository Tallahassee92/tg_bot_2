from dataclasses import dataclass
from environs import Env

@dataclass
class BotConfig:
    token: str
    admin_ids: list[int]

    @staticmethod
    def from_env(env: Env) -> "BotConfig":
        return BotConfig(
            token=env.str('BOT_TOKEN'),
            admin_ids=env.list('ADMIN_IDS', subcast=int)
        )

