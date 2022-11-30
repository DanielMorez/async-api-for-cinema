from pydantic import BaseSettings, PostgresDsn, RedisDsn, Field


class Settings(BaseSettings):
    pg_dsn: PostgresDsn
    redis_dsn: RedisDsn
    es_dsn: str
    etl_timeout: int
    es_indexes: list[str]
    time_format: str = '%Y-%m-%d %H:%M:%S.%f'
    load_chunk: int

    class Config:
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'
