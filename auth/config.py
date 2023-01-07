from pydantic import BaseSettings, RedisDsn, PostgresDsn, Field


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    pg_dsn: PostgresDsn
    project_name: str
    project_host: str = Field("0.0.0.0", env="AUTH_HOST")
    project_port: int = Field(5000, env="AUTH_PORT")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
