from abc import ABC, abstractmethod
from typing import Any

from api.v1.queries_params.base import QueryListBaseModel


class BaseService(ABC):
    def __init__(self, storage):
        self.storage = storage

    @abstractmethod
    def get_by_id(self, id: str) -> Any | None:
        pass

    @abstractmethod
    def get_list(self, params: QueryListBaseModel) -> list | None:
        pass
