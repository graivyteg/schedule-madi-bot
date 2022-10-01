from environs import Env
from dataclasses import dataclass
from typing import List


@dataclass
class TgBotConfig:
    token: str


@dataclass()
class DatabaseConfig:
    update_schedules: bool


@dataclass
class Config:
    tg_bot: TgBotConfig
    database: DatabaseConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        tg_bot=TgBotConfig(
            token=env.str('BOT_TOKEN')
        ),
        database=DatabaseConfig(
            update_schedules=env.bool('UPDATE_SCHEDULES')
        )
    )
