from pydantic import BaseSettings


class Config(BaseSettings):
    POLL_INTERVAL: float = 3
    DB_URL: str
    DEBUG: bool = True

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASSWORD: str
    MAX_RETRY_COUNT: int = 2


config = Config()
