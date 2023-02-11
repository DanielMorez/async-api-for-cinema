"""Настройки"""
import os

from pydantic import BaseSettings, Field, AnyUrl


ENV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BrokerSettings(BaseSettings):
    host: str
    port: int
    topic: str


class ClickHouseSettings(BaseSettings):
    host: str
    port: int
    password: str


class Settings(BaseSettings):
    project_name: str = Field("UGC", env="UGC_NAME")
    port: int = Field(8001, env="UGC_PORT")
    broker: BrokerSettings
    auth_dsn: AnyUrl
    clickhouse: ClickHouseSettings

    class Config:
        #  Для локальной разработки вне docker
        env_file = (
            os.path.join(ENV_DIR, ".env.prod"),
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "__"


settings = Settings()
