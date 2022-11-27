import os
from logging import config as logging_config

from pydantic.env_settings import BaseSettings
from pydantic.networks import RedisDsn

from core.logger import LOGGING

logging_config.dictConfig(LOGGING)


class Settings(BaseSettings):
    project_name: str
    redis_dsn: RedisDsn
    es_dsn: str
    base_dir: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    class Config:
        case_sensitive = False
        env_file = '../.env'
        env_file_encoding = 'utf-8'
