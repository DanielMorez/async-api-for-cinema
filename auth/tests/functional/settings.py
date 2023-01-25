from pydantic import BaseSettings, RedisDsn, AnyUrl, Field, PostgresDsn


class TestSettings(BaseSettings):
    redis_dsn: RedisDsn = Field("redis://127.0.0.1:6379", env="REDIS_DSN")
    pg_dsn: PostgresDsn = Field("redis://127.0.0.1:5432", env="PG_DSN")
    service_url: AnyUrl = Field("http://127.0.0.1:5001", env="AUTH_DSN")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
