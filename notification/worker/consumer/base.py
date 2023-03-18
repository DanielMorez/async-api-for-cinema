from abc import ABC, abstractmethod


class MessageBrokerConsumerClient(ABC):
    @abstractmethod
    def startup(self, *args, **kwargs):
        pass

    @abstractmethod
    def shutdown(self, *args, **kwargs):
        pass

    @abstractmethod
    def receive(self, *args, **kwargs):
        pass
