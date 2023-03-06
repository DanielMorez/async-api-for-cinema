from abc import ABC, abstractmethod


class EmailSenderAbstract(ABC):
    @abstractmethod
    def send(self, address: str, subject: str, data: str):
        pass
