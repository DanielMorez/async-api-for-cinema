import pika

from typing import Callable
from consumer.base import MessageBrokerConsumerClient


class RabbitMQConsumerClient(MessageBrokerConsumerClient):
    def __init__(
            self, host: str, port: int, user: str, password: str, queue: str, callback: Callable
    ):
        self._dsn = f"amqp://{user}:{password}@{host}:{port}"
        self._connection = pika.BlockingConnection(
            pika.URLParameters(self._dsn)
        )
        self._channel = self._connection.channel()
        self._queue = queue
        self._callback = callback

    def startup(self) -> None:
        self._channel.queue_declare(queue=self._queue)
        self._channel.basic_consume(
            queue=self._queue,
            on_message_callback=self._callback,
            auto_ack=True
        )

    def shutdown(self) -> None:
        self._connection.close()

    def receive(self) -> None:
        self._channel.start_consuming()
