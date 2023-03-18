from datetime import datetime
from enum import Enum

from sqlalchemy import JSON, Column, DateTime
from sqlalchemy import Enum as saEnum
from sqlalchemy import ForeignKey, Integer, String, Text

from db import Base


class DateMixin:
    """Вспомогательный миксин дат."""

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class TemplateCodes(Enum):
    """Коды шаблонов."""

    welcome_letter = "welcome_letter"
    selection_movies = "selection_movies"
    personal_newsletter = "personal_newsletter"


class Template(DateMixin, Base):
    """Модель шаблонов."""

    __tablename__ = "email_templates"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String, nullable=False)
    code = Column(saEnum(TemplateCodes))
    html = Column(Text, nullable=False)
    subject = Column(Text, nullable=False)


class NotificationStatuses(str, Enum):  # noqa: WPS600
    """Статусы уведомлений."""

    to_send = "to_send"
    in_process = "in_process"
    done = "done"
    cancelled = "cancelled"
    failed = "failed"


class Channels(str, Enum):  # noqa: WPS600
    """Канал передачи данных."""

    email = "email"


class Task(DateMixin, Base):
    """Уведомление пользователя."""

    __tablename__ = "email_tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    status = Column(saEnum(NotificationStatuses))
    email = Column(String, nullable=False)

    template_id = Column(Integer, ForeignKey('email_templates.id'))
    template_data = Column(JSON)

    scheduled_datetime = Column(DateTime)
    execution_datetime = Column(DateTime)
    retry_count = Column(Integer, default=0)

    error_message = Column(Text, nullable=True)
    hash_sum = Column(String, unique=True)
