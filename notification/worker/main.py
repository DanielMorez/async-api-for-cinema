import json
from contextlib import closing
from typing import Callable

from pika.adapters.blocking_connection import BlockingChannel
from psycopg2.extras import RealDictCursor

from auth.client import AuthClient
from config import settings
from consumer.rabbitmq import RabbitMQConsumerClient
from storage.postgres import PostgresClient
from storage.service import PostgresService


def callback_factory(service: PostgresService, auth_client: AuthClient) -> Callable:
    def callback(ch: BlockingChannel, method, properties, body: bytes) -> None:
        message = json.loads(body.decode('utf8'))
        print(" [x] Received %r" % body)
        # get template from postgres
        template = service.get_template_by_id(message["template_id"])
        # get personal data - email and name
        users = auth_client.get_personal_data_by_ids(message["user_ids"])
        if template.type == "email":
            a = 1
        # TODO: render template with jinja2
        # TODO: if template == email: send email
    return callback


def worker():
    with closing(PostgresClient(settings.pg_dsn, cursor_factory=RealDictCursor)) as pg_conn:
        pg_conn: PostgresClient

        service = PostgresService(pg_conn)
        auth_client = AuthClient(settings.auth_api)

        callback: Callable = callback_factory(service, auth_client)

        consumer = RabbitMQConsumerClient(callback=callback, **settings.rabbitmq.dict())
        consumer.startup()
        consumer.receive()


if __name__ == "__main__":
    worker()
