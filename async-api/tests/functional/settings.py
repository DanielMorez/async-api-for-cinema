from pydantic import BaseSettings, RedisDsn, AnyUrl, Field


class TestSettings(BaseSettings):
    es_dsn: AnyUrl = Field("http://127.0.0.1:9200", env="ES_DSN")
    es_index: str = Field("movies", env="ES_INDEX")
    es_id_field: str = Field("id")

    redis_dsn: RedisDsn = Field("redis://127.0.0.1:6379", env="REDIS_DSN")
    service_url: AnyUrl = Field("http://127.0.0.1:8000", env="ASYNC_API_DSN")


test_settings = TestSettings()
