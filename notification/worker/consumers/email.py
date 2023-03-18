import hashlib
import json
import logging
from datetime import datetime
from typing import Callable, Optional

import pika
from pika import channel as pika_channel  # noqa: F401

from config import settings
from consumers.base import ReconnectingConsumer
from services.task import get_task_service
from workers.email.handlers import handlers
from workers.email.logger import EmailEventAdapter
from workers.email.models import NotificationStatuses

logger = logging.getLogger(__name__)


def get_template_data(handler: Callable[[dict], dict], event_data: dict) -> dict:
    """Получает обогащенные данные."""
    return handler(event_data)


class EmailConsumer(ReconnectingConsumer):
    """Потребитель сообщений из RabbitMQ."""

    def __init__(self):
        parameters = {
            # "EXCHANGE": "", #settings.RABBIT_EMAIL_EXCHANGE,
            # "EXCHANGE_TYPE": "", #settings.RABBIT_EMAIL_EXCHANGE_TYPE,
            "QUEUES": settings.RABBITMQ__QUEUE,
            # "ROUTING_KEY": "", #settings.RABBIT_EMAIL_ROUTING_KEY,
            "USERNAME": settings.RABBITMQ__USER,
            "PASSWORD": settings.RABBITMQ__PASSWORD,
            "HOST": settings.RABBITMQ__HOST,
        }
        super().__init__(parameters)

    def decode_data(self, body: bytes, delivery_tag: int) -> Optional[dict]:
        """Сериализует JSON данные в Python объекты."""
        try:
            return json.loads(body)
        except json.decoder.JSONDecodeError as exc:
            logger.exception(exc)
            self._consumer.acknowledge_message(delivery_tag)
            return None

    def _get_hash_sum(self, data: dict) -> str:
        return hashlib.sha256(
            json.dumps(data, sort_keys=True).encode("utf-8"),
        ).hexdigest()

    def on_message(  # noqa: WPS231,WPS213
        self,
        _unused_channel: pika_channel.Channel,
        basic_deliver: pika.spec.Basic.Deliver,
        _properties: pika.spec.BasicProperties,
        body: bytes,
    ):
        """Обрабатывает сообщение из очереди."""
        event_data = self.decode_data(body, basic_deliver.delivery_tag)

        if event_data is None:
            self._consumer.acknowledge_message(basic_deliver.delivery_tag)

        adapter = EmailEventAdapter(logger, event_data)

        try:
            handler = handlers[event_data["event_type"]]
        except KeyError:
            adapter.info("Handler not found for this product.")
        else:
            adapter.info("Email handler found")
            adapter.debug(f"Email handler called with {event_data}")

            try:  # noqa: WPS505
                result = handler(event_data)
            except Exception as exc:
                adapter.exception(exc)
                self._consumer.acknowledge_message(basic_deliver.delivery_tag)
                return None

            task_service = get_task_service()

            for template_data in result["context"]:
                task_service.create_task(
                    email=template_data["email"],
                    scheduled_datetime=datetime.fromisoformat(
                        result["scheduled_datetime"],
                    ),
                    template_id=result["template_id"],
                    status=NotificationStatuses.to_send.value,
                    template_data=template_data,
                    hash_sum=self._get_hash_sum(result),
                )

            adapter.info("Notification successfully created")

        self._consumer.acknowledge_message(basic_deliver.delivery_tag)


# email_consumer = EmailConsumer()
