import json
import logging
from contextlib import closing
from typing import Callable

from pika.adapters.blocking_connection import BlockingChannel
from psycopg2.extras import RealDictCursor

from auth.client import AuthClient
from config import settings
from consumer.rabbitmq import RabbitMQConsumerClient
from helpers.email import send_common_email, send_personal_email
from storage.postgres import PostgresClient
from storage.service import PostgresService


logging.basicConfig()
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def callback_factory(service: PostgresService, auth_client: AuthClient) -> Callable:
    def callback(ch: BlockingChannel, method, properties, body: bytes) -> None:
        message = json.loads(body.decode('utf8'))
        logger.info(f"Received {body}")
        # get template from postgres
        template = service.get_template_by_id(message["template_id"])
        # get personal data - email and name
        users = auth_client.get_personal_data_by_ids(message["user_ids"])
        if template.type == "email":
            if template.is_personal:
                for user in users:
                    try:
                        send_personal_email(user, template)
                    except Exception as error:
                        logger.error(f"Got some error {error}")
            else:
                user_emails = [user.email for user in users]
                send_common_email(user_emails, template)
    return callback


def worker():
    with closing(PostgresClient(settings.pg_dsn, cursor_factory=RealDictCursor)) as pg_conn:
        pg_conn: PostgresClient

        service = PostgresService(pg_conn)
        auth_client = AuthClient(settings.auth_api)

        callback: Callable = callback_factory(service, auth_client)

        consumer = RabbitMQConsumerClient(callback=callback, **settings.rabbitmq.dict())
        consumer.startup()
        logger.info("Start worker!")
        consumer.receive()


if __name__ == "__main__":
    worker()
