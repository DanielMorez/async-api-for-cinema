"""Модуль содержит основные обработчики для UGC событий."""
import httpx

from config import settings
from services.template import get_template_service


def selection_movies(event_data: dict) -> dict:
    """Обработчик для события 'Подборка фильмов'."""
    payload = event_data["payload"]
    user_ids: list[str] = payload["user_ids"]
    movie_ids: list[str] = payload["movie_ids"]
    event_type: str = event_data["event_type"]

    response = httpx.post(
        f"{settings.url_auth_service}/auth/user_ids_bulk/",
        json=[user_ids],
    )
    person_json_data = response.json()

    response = httpx.post(f"{settings.url_movie_service}/movies/", json=[movie_ids])
    movies_json_data = response.json()

    movie_info = [movie["title"] for movie in movies_json_data]

    # Template
    service = get_template_service()
    template = service.get_template_by_event_type(event_type=event_type)

    return {
        "context": [
            {
                "movies": movie_info,
                "first_name": person["first_name"],
                "last_name": person["last_name"],
                "email": person["email"],
            }
            for person in person_json_data
        ],
        "scheduled_datetime": event_data["scheduled_datetime"],
        "template_id": template.id,
    }


def personal_newsletter(event_data: dict) -> dict:
    """Обработчик для события 'Личная рассылка'."""
    payload = event_data["payload"]
    user_id: str = payload["user_id"]
    movie_ids: list[str] = payload["movie_ids"]
    event_type: str = event_data["event_type"]

    response = httpx.post(
        f"{settings.url_auth_service}/auth/user_ids_bulk/",
        json=[user_id],
    )
    person_json_data = response.json()[0]

    response = httpx.post(f"{settings.url_movie_service}/movies/", json=[movie_ids])
    movies_json_data = response.json()

    movie_info = [movie["title"] for movie in movies_json_data]

    # Template
    service = get_template_service()
    template = service.get_template_by_event_type(event_type=event_type)

    return {
        "context": [
            {
                "movies": movie_info,
                "first_name": person_json_data["first_name"],
                "last_name": person_json_data["last_name"],
                "email": person_json_data["email"],
            },
        ],
        "scheduled_datetime": event_data["scheduled_datetime"],
        "template_id": template.id,
    }


handlers = {
    "selection_movies": selection_movies,
    "personal_newsletter": personal_newsletter,
}
