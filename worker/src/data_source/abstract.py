from abc import ABC, abstractmethod
from typing import Callable, Optional

from pika.adapters.blocking_connection import BlockingChannel


class DataSourceAbstract(ABC):

    @abstractmethod
    def _connect(self):
        pass

    @abstractmethod
    def decode_data(self, body: bytes) -> Optional[dict]:
        pass

    @abstractmethod
    def callback_factory(self, channel: BlockingChannel) -> Callable:
        pass
