from abc import ABC

from sqlalchemy.orm import Session


class AbstractService(ABC):
    """Базовый класс сервисов."""

    def __init__(self, session: Session) -> None:
        self._session = session

    def close(self) -> None:
        """Завершает работу сервиса."""
        self._session.close()
