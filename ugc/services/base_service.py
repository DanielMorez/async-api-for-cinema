from abc import ABC, abstractmethod
from uuid import UUID


class BaseService(ABC):
    @abstractmethod
    def __init__(self, client, *args, **kwargs):
        self._conn = client

    @abstractmethod
    async def add_bookmark(self, user_id: UUID, film_id: UUID) -> None:
        pass

    @abstractmethod
    async def remove_bookmark(self, user_id: UUID, bookmark_id: UUID) -> None:
        pass

    @abstractmethod
    async def user_bookmarks(self, user_id) -> list[dict]:
        pass

    @abstractmethod
    async def rate_film(self, film_id: UUID, user_id: UUID, stars: int) -> None:
        pass

    @abstractmethod
    async def film_rating(self, film_id: UUID) -> dict:
        pass

    @abstractmethod
    async def add_review(self, film_id: UUID, user_id: UUID, text: str) -> None:
        pass

    @abstractmethod
    async def remove_review(self, review_id: str, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def like_review(self, film_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def dislike_review(self, film_id: UUID, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def reviews(self, film_id: UUID) -> list[dict]:
        pass
