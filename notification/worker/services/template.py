from contextlib import contextmanager
from typing import Optional

from sqlalchemy.orm import Session

from db import SessionLocal
from services.abstract import AbstractService
from workers.email.models import Template


@contextmanager
def service_with_session(session: Session):
    """Возвращает подготовленный сервис."""
    service = TemplateService(session)
    yield service
    service.close()


class TemplateService(AbstractService):
    """Сервис по работе с моделью Template."""

    def get_template_by_event_type(self, event_type: str) -> Optional[Template]:
        """Получает Template экземпляр по типу события."""
        return self._session.query(Template).filter_by(code=event_type).one_or_none()


def get_template_service() -> TemplateService:
    """Возвращает подготовленный TemplateService."""
    with service_with_session(SessionLocal()) as service:
        return serdvice
