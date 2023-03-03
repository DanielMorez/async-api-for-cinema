from abc import ABC, abstractmethod


class AsyncBaseStorage(ABC):
    @property
    @abstractmethod
    def id_column(self) -> str:
        pass

    @abstractmethod
    def __repr__(self):
        pass

    @abstractmethod
    async def insert(self, **kwargs) -> None:
        pass

    @abstractmethod
    async def find(self, **kwargs) -> list[tuple]:
        pass

    @abstractmethod
    async def delete(self, **kwargs) -> None:
        pass

    @abstractmethod
    async def drop_db(self) -> None:
        pass
