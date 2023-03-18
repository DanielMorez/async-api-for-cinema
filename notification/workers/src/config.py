from pydantic import BaseSettings


class Settings(BaseSettings):
    """Основные настройки приложения."""

    sleep_time: int = 10
    log_level: str = "INFO"
    default_timeout_for_requests: int = 2

    rabbit_email_exchange: str
    rabbit_email_exchange_type: str
    rabbit_email_queues: list[str]
    rabbit_email_routing_key: str
    rabbit_username: str
    rabbit_password: str
    rabbit_host: str

    postgres_db: str
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str

    url_auth_service: str
    url_movie_service: str

    @property
    def database_uri(self):
        """Возвращает URI базы данных."""
        return f"postgresql://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"  # noqa: WPS322, E501


settings = Settings()
