from abc import ABC, abstractmethod
from typing import List


class UserServiceClientAbstract(ABC):
    @abstractmethod
    def get_users_for_category(self, category: str) -> List[str]:
        pass
