"""Модуль для работы с брокером сообщений"""

import json
from abc import ABC, abstractmethod

from aiokafka import AIOKafkaConsumer, AIOKafkaProducer


producer: "MessageBrokerProducerClient" = None
consumer: "MessageBrokerConsumerClient" = None


async def get_producer() -> "MessageBrokerProducerClient":
    return producer


async def get_consumer() -> "MessageBrokerConsumerClient":
    return consumer


def json_serializer(data):
    return json.dumps(data).encode()


def json_deserializer(data):
    return json.loads(data.decode())


class MessageBrokerProducerClient(ABC):
    @abstractmethod
    def startup(self, *args, **kwargs):
        """Метод инициализации"""
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        """Метод завершения"""
        pass

    @abstractmethod
    def send(self, topic, message, key):
        """Метод отправки сообщения в шину"""
        pass


class MessageBrokerConsumerClient(ABC):
    @abstractmethod
    def startup(self, *args, **kwargs):
        """Метод инициализации"""
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        """Метод завершения"""
        pass

    @abstractmethod
    def receive(self, topic, message, key):
        """Метод получения сообщения из шины"""
        pass


class KafkaProducerClient(MessageBrokerProducerClient):
    def __init__(self, bootstrap_servers) -> None:
        self._producer = None
        self._bootstrap_servers = bootstrap_servers

    async def startup(
        self, key_serializer=json_serializer, value_serializer=json_serializer
    ):
        """Метод инициализации"""

        if self._producer:
            return

        self._producer = AIOKafkaProducer(
            bootstrap_servers=self._bootstrap_servers,
            key_serializer=key_serializer,
            value_serializer=value_serializer,
        )
        await self._producer.start()

    async def shutdown(self):
        """Метод завершения"""
        if self._producer:
            await self._producer.stop()
            self._producer = None

    async def send(self, topic, message, key):
        """Метод получения сообщения из шины"""

        if not self._producer:
            await self.startup()

        await self._producer.send_and_wait(topic, message, key)


class KafkaConsumerClient(MessageBrokerConsumerClient):
    def __init__(
        self, bootstrap_servers, topic, group_id=None, take_oldest=False
    ) -> None:
        self._consumer = None
        self._bootstrap_servers = bootstrap_servers
        self._topic = topic
        self._group_id = group_id
        self._auto_offset_reset = "earliest" if take_oldest is True else "latest"

    async def startup(
        self,
        key_deserializer=json_deserializer,
        value_deserializer=json_deserializer,
    ):
        """Метод инициализации"""

        if self._consumer:
            return

        self._consumer = AIOKafkaConsumer(
            self._topic,
            group_id=self._group_id,
            bootstrap_servers=self._bootstrap_servers,
            auto_offset_reset=self._auto_offset_reset,
            key_deserializer=key_deserializer,
            value_deserializer=value_deserializer,
        )
        await self._consumer.start()

    async def shutdown(self):
        """Метод завершения"""
        if self._consumer:
            await self._consumer.stop()
            self._consumer = None

    async def receive(self):
        """Метод получения сообщения из шины"""

        if not self._consumer:
            await self.startup()

        async for message in self._consumer:
            yield message
