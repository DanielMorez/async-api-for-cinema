from flask import Flask
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from config import Settings

settings = Settings()
limiter = Limiter(
    get_remote_address,
    default_limits=settings.auth_default_limits,
    storage_uri=settings.redis_dsn,
)


def init_limiter(app: Flask):
    limiter.init_app(app)
