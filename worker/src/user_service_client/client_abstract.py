from abc import ABC, abstractmethod

from pydantic.main import BaseModel


class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    promo_agree: bool
    category: str
    films_month_count: int
    favourite_genre: str


class UserServiceClientAbstract(ABC):
    @abstractmethod
    def get_user(self, user_id: str) -> UserInfo:
        pass
