from pydantic import BaseSettings, RedisDsn, PostgresDsn, Field


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    pg_dsn: PostgresDsn
    pg_schema: str = Field("auth", env="AUTH_PG_DEFAULT_SCHEMA")
    name: str = Field("auth")
    host: str = Field("0.0.0.0", env="AUTH_HOST")
    port: int = Field(5000, env="AUTH_PORT")
    debug: bool = Field(False, env="DEBUG")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
