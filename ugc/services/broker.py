from abc import ABC, abstractmethod
from functools import lru_cache

from fastapi import Depends

from adapters.broker import (
    MessageBrokerProducerClient,
    get_producer,
    MessageBrokerConsumerClient,
    get_consumer,
)
from core.config import settings


class BaseBrokerService(ABC):
    def __init__(
        self,
        producer: MessageBrokerProducerClient,
        consumer: MessageBrokerConsumerClient,
        topic: str,
    ):
        self._producer = producer
        self._consumer = consumer
        self._topic = topic

    @abstractmethod
    async def send_message(self, key, message):
        pass

    @abstractmethod
    async def get_messages(self, key):
        pass


class BrokerKafkaService(BaseBrokerService):
    def __init__(self, *args, **kwargs):
        super(BrokerKafkaService, self).__init__(*args, **kwargs)

    async def send_message(self, key, message):
        await self._producer.send(self._topic, message, key)

    async def get_messages(self, key):
        # TODO: method to get messages
        pass


@lru_cache()
def get_broker_service(
    producer: MessageBrokerProducerClient = Depends(get_producer),
    consumer: MessageBrokerConsumerClient = Depends(get_consumer),
) -> BaseBrokerService:
    return BrokerKafkaService(producer, consumer, settings.broker.topic)
