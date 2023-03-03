"""Настройки"""
import os

from pydantic import AnyUrl, BaseSettings, Field

ENV_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class BrokerSettings(BaseSettings):
    host: str
    port: int
    topic: str


class ClickHouseSettings(BaseSettings):
    host: str
    port: int
    password: str


class LogstashSettings(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    project_name: str = Field("UGC", env="UGC_NAME")
    port: int = Field(8001, env="UGC_PORT")
    broker: BrokerSettings
    auth_dsn: AnyUrl
    clickhouse: ClickHouseSettings
    logstash: LogstashSettings
    logstash_enable: bool = Field(False)
    sentry_dsn: AnyUrl = Field(None)

    class Config:
        #  Для локальной разработки вне docker
        env_file = (
            os.path.join(ENV_DIR, ".env.prod"),
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "__"


settings = Settings()
