from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbit_events_queue_name: str = 'email'
    rabbit_events_exchange_name: str = 'email'

    rabbit_username: str = 'rabbit'
    rabbit_password: str = 'rabbit'
    rabbit_host: str = 'fake_netflix_notification_rabbitmq'

    rabbit_exchange: str = 'email'
    rabbit_exchange_type: str = 'direct'

    log_level: str = 'INFO'

    user_registration_template: int = 1


settings = Settings()
