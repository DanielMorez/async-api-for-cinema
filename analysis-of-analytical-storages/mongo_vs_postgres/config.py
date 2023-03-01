from pydantic import BaseSettings, PostgresDsn, MongoDsn


class Settings(BaseSettings):
    PG_DSN: PostgresDsn
    MONGO_DSN: MongoDsn
    MONGO_DB: str

    class Config:
        case_sensitive = False
        env_file = "../.env"
        env_file_encoding = "utf-8"


settings = Settings()
