from abc import ABC, abstractmethod
from typing import Any, Dict


class ContextCollectorAbstract(ABC):
    @abstractmethod
    def collect(self, user_id: str) -> Dict[Any, Any]:
        pass
