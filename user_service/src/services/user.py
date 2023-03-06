import json
from abc import ABC, abstractmethod
from functools import lru_cache
from typing import List

from core.exceptions import NotFoundError
from models.user import UserInfo


class AbstractUserService(ABC):
    @abstractmethod
    async def get_by_id(self, user_id: str) -> UserInfo:
        pass

    @abstractmethod
    async def get_by_category(self, category_name: str) -> List[UserInfo]:
        pass


class UserService(AbstractUserService):

    def __get_user_data(self) -> List[UserInfo]:
        with open('fixtures/users.json', 'r') as file:
            data = json.load(file)
        return [UserInfo(**item) for item in data['users']]

    async def get_by_id(self, user_id: str) -> UserInfo:
        users = self.__get_user_data()
        for user in users:
            if user.id == user_id:
                return user
        raise NotFoundError(f'User {user_id} not found')

    async def get_by_category(self, category_name: str) -> List[UserInfo]:
        users = self.__get_user_data()
        return [user for user in users if user.category == category_name]


@lru_cache()
def get_user_service() -> AbstractUserService:
    return UserService()
