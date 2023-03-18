import os

from pydantic import BaseSettings, Field, PostgresDsn, AnyUrl


ENV_DIR = os.path.dirname(os.path.abspath(__file__))


class RabbitMQ(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    queue: str = Field("service.notifications")


class Settings(BaseSettings):
    project_name: str = Field("Notification Worker", env="NOTIFICATION_WORKER_NAME")
    pg_dsn: PostgresDsn = Field(env="PG_DSN")
    auth_api: AnyUrl = Field(env="AUTH_DSN")
    rabbitmq: RabbitMQ

    class Config:
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "__"


settings = Settings()
