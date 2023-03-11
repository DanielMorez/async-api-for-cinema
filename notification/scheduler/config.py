import os

from pydantic import BaseSettings, Field, PostgresDsn, AnyUrl

ENV_DIR = os.path.abspath(__file__)


class Settings(BaseSettings):
    project_name: str = Field("Notification Scheduler", env="NOTIFICATION_SCHEDULER_NAME")
    notification_api: AnyUrl = Field(env="NOTIFICATION_API_DSN")
    pg_dsn: PostgresDsn = Field(env="PG_DSN")

    class Config:
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )


settings = Settings()
