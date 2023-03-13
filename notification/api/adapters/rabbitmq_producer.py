from aio_pika import connect_robust, Message

from adapters.base_producer import MessageBrokerProducerClient
from cores.backoff import backoff, reconnect
from cores.serializers import json_serializer


class RabbitMQProducerClient(MessageBrokerProducerClient):
    def __init__(self, host: str, port: int, user: str, password: str, queue: str) -> None:
        self._dsn = f"amqp://{user}:{password}@{host}:{port}"
        self._connection = None
        self._channel = None
        self._queue = queue

    @property
    async def is_connected(self) -> bool:
        is_closed = self._channel.is_closed
        return not is_closed

    @backoff()
    async def connect(self) -> None:
        if not self._connection or self._connection.is_closed:
            self._connection = await connect_robust(self._dsn)
        if not self._channel or not await self.is_connected:
            self._channel = await self._connection.channel()

    async def startup(self) -> None:
        await self.connect()
        await self._channel.declare_queue(self._queue)

    @backoff()
    async def shutdown(self) -> None:
        if self._connection:
            await self._connection.close()
        self._connection = None

    @backoff()
    @reconnect
    async def send(self, message: dict) -> None:
        await self._channel.default_exchange.publish(
            Message(json_serializer(message)),
            routing_key=self._queue,
        )

    async def reconnect(self) -> None:
        if not await self.is_connected:
            await self.connect()
