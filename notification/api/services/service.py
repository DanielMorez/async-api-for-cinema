from functools import lru_cache

from fastapi import Depends

from adapters import get_producer
from adapters.base_producer import MessageBrokerProducerClient
from services.base_service import BaseBrokerService
from services.rabbitmq import BrokerRabbitMQService


@lru_cache()
def get_broker_service(
    producer: MessageBrokerProducerClient = Depends(get_producer)
) -> BaseBrokerService:
    return BrokerRabbitMQService(producer)
