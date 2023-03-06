import logging

from config import config
from data_source.rabbitmq import DataSourceRabbitMQ
from db.postgres import Postgres
from email_sender.factory import EmailSenderFactory
from user_service_client.client import UserServiceClient
from worker import Worker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    postgres = Postgres()
    user_service_client = UserServiceClient()
    email_sender = EmailSenderFactory.get_sender(config.EMAIL_SENDER_TYPE)

    worker = Worker(
        postgres=postgres,
        user_service_client=user_service_client,
        email_sender=email_sender
    )

    while True:
        consumer = DataSourceRabbitMQ(worker)
        consumer.listen_events()


if __name__ == '__main__':
    main()
