import logging
from contextlib import contextmanager

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from db import SessionLocal
from services.abstract import AbstractService
from workers.email.models import Task

logger = logging.getLogger(__name__)


@contextmanager
def service_with_session(session: Session):
    """Возвращает подготовленный сервис."""
    service = TaskService(session)
    yield service
    service.close()


class TaskService(AbstractService):
    """Сервис по работе с моделью Task."""

    def create_task(self, **kwargs) -> None:
        """Создает экземпляр Task."""
        task = Task(**kwargs)
        self._session.add(task)
        try:
            self._session.commit()
        except IntegrityError as exc:
            logger.exception(exc)


def get_task_service() -> TaskService:
    """Возвращает подготовленный TemplateService."""
    with service_with_session(SessionLocal()) as service:
        return service
