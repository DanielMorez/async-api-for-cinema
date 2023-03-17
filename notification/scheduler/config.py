import os

from pydantic import BaseSettings, Field, PostgresDsn, AnyUrl

ENV_DIR = os.path.dirname(os.path.abspath(__file__))


class Settings(BaseSettings):
    project_name: str = Field("Notification Scheduler", env="NOTIFICATION_SCHEDULER_NAME")
    notification_api: AnyUrl = Field(env="NOTIFICATION_API_DSN")
    auth_api: AnyUrl = Field(env="AUTH_DSN")
    pg_dsn: PostgresDsn = Field(env="PG_DSN")

    extract_chunk: int = Field(1000)
    time_interval: int = Field(5)

    class Config:
        env_file_encoding = "utf-8"
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            # os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )


settings = Settings()
