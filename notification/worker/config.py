import os
from typing import List
from pydantic import BaseSettings, Field, PostgresDsn, AnyUrl

ENV_DIR = os.path.abspath(__file__)


class Settings(BaseSettings):
    project_name: str = Field("Notification Worker", env="NOTIFICATION_WORKER_NAME")
    pg_dsn: PostgresDsn = Field(env="PG_DSN")
    auth_dsn: AnyUrl = Field(env="AUTH_DSN")

    sleep_time: int = 10
    log_level: str = "INFO"
    default_timeout_for_requests: int = 2

    RABBITMQ__QUEUE: str
    RABBITMQ__USER: str
    RABBITMQ__PASSWORD: str
    RABBITMQ__HOST: str
    RABBITMQ__PORT: str

    PG_DB_NAME: str
    PG_HOST: str
    PG_PORT: int
    PG_USER: str
    PG_PASSWORD: str
    PG_DSN: str

    url_auth_service: str
    url_movie_service: str


    class Config:
        env_file = (
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env_test.dev"),
            os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "RABBITMQ__"

    @property
    def database_uri(self):
        """Возвращает URI базы данных."""
        return self.PG_DSN  # noqa: WPS322, E501


settings = Settings()