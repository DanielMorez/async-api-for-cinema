import os

from pydantic import BaseSettings, Field, PostgresDsn


ENV_DIR = os.path.abspath(__file__)


class Settings(BaseSettings):
    project_name: str = Field("Notification Admin Panel", env="NOTIFICATION_ADMIN_NAME")
    port: int = Field(8003, env="NOTIFICATION_ADMIN_PORT")
    pg_dsn: PostgresDsn = Field(env="PG_DSN")

    class Config:
        env_file = (
            os.path.join(ENV_DIR, ".env.dev"),
            os.path.join(ENV_DIR, ".env"),  # Если запускаем весь проект
        )


settings = Settings()
