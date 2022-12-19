from abc import ABC, abstractmethod


class AsyncSearchStorage(ABC):
    @abstractmethod
    async def get(self, *args, **kwargs):
        pass

    @abstractmethod
    async def search(self, key: str, value: str, expire: int, **kwargs):
        pass
