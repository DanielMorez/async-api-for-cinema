import os

from oauthlib.oauth2 import WebApplicationClient
from pydantic import BaseSettings, RedisDsn, PostgresDsn, Field, AnyUrl


class Settings(BaseSettings):
    redis_dsn: RedisDsn = Field(None)
    pg_dsn: PostgresDsn = Field(None)
    pg_schema: str = Field("auth", env="AUTH_PG_DEFAULT_SCHEMA")
    name: str = Field("auth")
    host: str = Field("0.0.0.0", env="AUTH_HOST")
    port: int = Field(5000, env="AUTH_PORT")
    debug: bool = Field(False, env="DEBUG")
    jwt_secrete_key: str = Field("foo", env="JWT_SECRETE_KEY")
    jwt_cookie_secure: str = Field(False, env="JWT_COOKIE_SECURE")
    jwt_token_location: list = Field(["headers"], env="JWT_TOKEN_LOCATION")
    jwt_access_token_expires: int = Field(10 * 60, env="JWT_ACCESS_TOKEN_EXPIRES")
    jwt_refresh_token_expires: int = Field(
        60 * 60 * 24, env="JWT_REFRESH_TOKEN_EXPIRES"
    )
    auth_limiter_enable: bool = Field(False, env="AUTH_LIMITER_ENABLE")
    auth_default_limits: list = Field([], env="AUTH_DEFAULT_LIMITS")
    request_id_enable: bool = Field(False, env="REQUEST_ID_ENABLE")
    jaeger_host: str = Field("localhost", env="JAEGER_HOST")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")

    GOOGLE_CLIENT_ID: str = Field("", env="GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET: str = Field("", env="GOOGLE_CLIENT_SECRET")
    GOOGLE_DISCOVERY_URL: str = Field("", env="GOOGLE_DISCOVERY_URL")

    logstash_enable: bool = Field(False, env="LOGSTASH_ENABLE")
    logstash_dsn: AnyUrl = Field("", env="LOGSTASH_DSN")
    sentry_dsn: AnyUrl = Field(None, env="SENTRY_DSN")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
client = WebApplicationClient(settings.GOOGLE_CLIENT_ID)

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
