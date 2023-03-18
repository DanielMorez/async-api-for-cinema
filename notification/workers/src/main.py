import logging
from typing import Optional

from notification.worker.consumers.email import EmailConsumer

logger = logging.getLogger(__name__)


class Handler:
    """Основной обработчик."""

    def __init__(self):
        self._email_consumer: Optional[EmailConsumer] = None

    def on_startup(self):
        """Запускает и инициализирует вспомогательные сервисы перед запуском."""
        self._email_consumer = EmailConsumer()

    def start(self):
        """Запускает потребителя."""
        logger.info("Запуск email потребителя")
        self._email_consumer.consume()


if __name__ == "__main__":
    handler = Handler()
    handler.on_startup()
    handler.start()
