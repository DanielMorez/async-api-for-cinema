from abc import ABC, abstractmethod


class MessageBrokerProducerClient(ABC):
    @abstractmethod
    async def startup(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def shutdown(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def send(self, message: dict) -> None:
        pass

    @abstractmethod
    async def reconnect(self) -> None:
        pass

    @abstractmethod
    async def connect(self) -> None:
        pass

    @property
    @abstractmethod
    async def is_connected(self) -> bool:
        pass
