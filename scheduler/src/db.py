import datetime
import logging
from typing import Optional

import backoff
import sqlalchemy.exc
from config import config
from models import NotificationStatuses
from sqlalchemy import MetaData, Table, create_engine, select, update
from sqlalchemy.engine import Connection, Engine

logger = logging.getLogger(__name__)
meta = MetaData()
_engine: Engine = None
_connection: Connection = None
notifications = None
templates = None


def get_template_by_id(template_id: str) -> Optional[dict]:
    query = select(templates).where(templates.c.id == template_id)
    resultset = _connection.execute(query)
    template = resultset.mappings().first()
    logger.debug(f"got template: {template}")
    return template


def init():
    logger.debug("Init db module")
    global _engine
    _engine = create_engine(config.DB_URL)

    @backoff.on_exception(backoff.expo, sqlalchemy.exc.SQLAlchemyError)
    def _connect_to_db():
        global _connection, notifications, templates
        _connection = _engine.connect()
        notifications = Table("email_tasks", meta, autoload_with=_engine)
        templates = Table("email_templates", meta, autoload_with=_engine)

    _connect_to_db()


def read_notifications_chunk(size=100) -> list[dict]:
    """Returns oldest notifications from db that should be sent."""
    logger.debug(f"reading notifications from db")
    trans = _connection.begin()
    query = (
        select(notifications)
        .with_for_update(skip_locked=True)
        .where(
            notifications.c.status == NotificationStatuses.to_send,
            notifications.c.scheduled_datetime < datetime.datetime.now(),
        )
        .limit(size)
    )
    resultset = _connection.execute(query)
    notifications_objects = resultset.mappings().all()
    n_ids = [n["id"] for n in notifications_objects]
    query = (
        update(notifications)
        .where(notifications.c.id.in_(n_ids))
        .values(status=NotificationStatuses.in_process)
    )
    _connection.execute(query)
    trans.commit()
    logger.debug(f"read {len(notifications_objects)} notifications")
    logger.debug(f"received notifications: {notifications_objects}")
    return notifications_objects


def mark_notification_as_sent(notification_id):
    query = (
        update(notifications)
        .where(notifications.c.id == notification_id)
        .values(status=NotificationStatuses.done)
    )
    _connection.execute(query)


def drop_or_resend_notification(notification_id):
    # Если шедулер достает сообщение с to_resend и не получается переотправить,
    # то он проверяет retry_count, если он больше MAX_RESEND, то меняет статус на FAILED.
    query = select(notifications).where(notifications.c.id == notification_id)
    notification = _connection.execute(query).mappings().first()
    if not notification:
        logger.error(f"Notification {notification_id} disappeared!")
        return

    if notification["retry_count"] == config.MAX_RETRY_COUNT:
        logger.info(
            f"Stop trying to send notification {notification_id}, as retry_count exceeded max"
        )
        update(notifications).where(notifications.c.id == notification_id).values(
            status=NotificationStatuses.failed
        )
        return

    update(notifications).where(notifications.c.id == notification_id).values(
        status=NotificationStatuses.to_send, retry_count=notification["retry_count"] + 1
    )
    logger.info(f"Trying to send notification {notification_id} again")
