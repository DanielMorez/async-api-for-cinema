import os
from logging import config as logging_config

from pydantic import Field
from pydantic.env_settings import BaseSettings
from pydantic.networks import RedisDsn, AnyUrl

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str
    redis_dsn: RedisDsn
    es_dsn: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    cache_expire_in_seconds: int = Field(60 * 5)  # 5 minutes
    auth_dsn: AnyUrl = Field("0.0.0.0:5001")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"
