"""Настройки"""

import os

from pydantic import BaseSettings


ENV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class BrokerSettings(BaseSettings):
    host: str
    port: int
    topic: str


class Settings(BaseSettings):
    broker: BrokerSettings

    class Config:
        #  Для локальной разработки вне docker
        env_file = (
            os.path.join(ENV_DIR, ".env.prod"),
            os.path.join(ENV_DIR, ".env.dev"),
        )
        env_nested_delimiter = "__"


settings = Settings()
