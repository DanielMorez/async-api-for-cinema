from abc import ABC, abstractmethod
from typing import Any, Dict


class PublisherAbstract(ABC):
    @abstractmethod
    def publish(self, data: Dict[Any, Any]):
        pass
