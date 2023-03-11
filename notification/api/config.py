import os

from pydantic import BaseSettings, Field


ENV_DIR = os.path.abspath(__file__)


class RabbitMQ(BaseSettings):
    host: str
    port: int


class Settings(BaseSettings):
    project_name: str = Field("Notification API", env="NOTIFICATION_ADMIN_NAME")
    port: int = Field(8003, env="NOTIFICATION_API_PORT")
    rabbitmq_dsn: RabbitMQ

    class Config:
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "__"


settings = Settings()
