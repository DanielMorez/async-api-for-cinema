from abc import ABC, abstractmethod


class BaseStorage(ABC):
    @property
    @abstractmethod
    def required_dict_reader(self) -> bool:
        """Define a method to read from csv"""
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

    @abstractmethod
    async def aggregate(self, **kwargs) -> list[tuple]:
        pass
