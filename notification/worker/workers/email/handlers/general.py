"""Модуль содержит основные обработчики для основных событий."""
import httpx

from config import settings
from services.template import get_template_service


def welcome_letter(event_data: dict) -> dict:  # noqa: WPS210
    """Обработчик для события 'Приветственное письмо'."""
    payload = event_data["payload"]
    user_id: str = payload["user_id"]
    event_type: str = event_data["event_type"]

    response = httpx.post(
        f"{settings.url_auth_service}/auth/user_ids_bulk/",
        json=[user_id],
    )
    json_data = response.json()[0]

    # Template
    service = get_template_service()
    template = service.get_template_by_event_type(event_type=event_type)

    return {
        "context": [
            {
                "first_name": json_data["first_name"],
                "last_name": json_data["last_name"],
                "email": json_data["email"],
            },
        ],
        "scheduled_datetime": event_data["scheduled_datetime"],
        "template_id": template.id,
    }


handlers = {"welcome_letter": welcome_letter}
