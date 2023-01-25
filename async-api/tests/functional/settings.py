from pydantic import BaseSettings, RedisDsn, AnyUrl, Field


class TestSettings(BaseSettings):
    es_dsn: AnyUrl = Field("http://127.0.0.1:9200", env="ES_DSN")
    redis_dsn: RedisDsn = Field("redis://127.0.0.1:6379", env="REDIS_DSN")
    service_url: AnyUrl = Field("http://127.0.0.1:8000", env="ASYNC_API_DSN")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


test_settings = TestSettings()
