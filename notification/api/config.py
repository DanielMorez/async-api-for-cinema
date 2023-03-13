import os

from pydantic import BaseSettings, Field


ENV_DIR = os.path.dirname(os.path.abspath(__file__))


class RabbitMQ(BaseSettings):
    host: str
    port: int
    user: str
    password: str
    queue: str = Field("notifications")


class Settings(BaseSettings):
    project_name: str = Field("Notification API", env="NOTIFICATION_API_NAME")
    port: int = Field(8003, env="NOTIFICATION_API_PORT")
    rabbitmq: RabbitMQ

    class Config:
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )
        env_nested_delimiter = "__"
        case_sensitive = False


settings = Settings()
