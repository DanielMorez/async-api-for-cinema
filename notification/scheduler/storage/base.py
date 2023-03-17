from abc import ABC, abstractmethod
from typing import Any

from pydantic import AnyUrl

from logging import getLogger

logger = getLogger(__name__)


class ClientInterface(ABC):
    @property
    @abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def reconnect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError


class BaseClient(ClientInterface, ABC):
    _connection: Any

    def __init__(self, dsn: AnyUrl, *args, **kwargs):
        self.dsn = dsn
        self.args = args
        self.kwargs = kwargs
        self.connect()

    def __repr__(self):
        return f"{self.__class__.__name__} with dsn: {self.dsn}"

    @property
    @abstractmethod
    def is_connected(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def connect(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def reconnect(self) -> None:
        if not self.is_connected:
            logger.info(f"Trying to reconnect to: {self}.")
            self.connect()

    @abstractmethod
    def close(self) -> None:
        if self.is_connected:
            self._connection.close()
            logger.info(f"Closed connection for: {self}.")

        self._connection = None
