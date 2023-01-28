from pydantic import BaseSettings, RedisDsn, PostgresDsn, Field


class Settings(BaseSettings):
    redis_dsn: RedisDsn
    pg_dsn: PostgresDsn
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
    auth_default_limits: list = Field([], env="AUTH_DEFAULT_LIMITS")
    request_id_enable: bool = Field(False, env="REQUEST_ID_ENABLE")
    jaeger_host: str = Field("localhost", env="JAEGER_HOST")
    jaeger_port: int = Field(6831, env="JAEGER_PORT")

    class Config:
        case_sensitive = False
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
