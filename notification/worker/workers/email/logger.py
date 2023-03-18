from logging import LoggerAdapter


class EmailEventAdapter(LoggerAdapter):
    """Адаптер для email."""

    def process(self, msg, kwargs):
        """Процесс логирования сообщений."""
        service = self.extra.get("service")
        event_type = self.extra.get("event_type")

        return f"[service={service}] [event_type={event_type}] {msg}", kwargs
