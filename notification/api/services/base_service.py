from abc import ABC, abstractmethod

from adapters import MessageBrokerProducerClient


class BaseBrokerService(ABC):
    def __init__(self, producer: MessageBrokerProducerClient):
        self._producer = producer

    @abstractmethod
    async def send_message(self, message):
        pass
