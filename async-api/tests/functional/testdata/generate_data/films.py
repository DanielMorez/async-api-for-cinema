import uuid
from datetime import datetime


def generate_films(amount: int = 60) -> list[dict]:
    films = [generate_film() for i in range(amount)]
    return films


def generate_film() -> dict:
    film = {
        "id": str(uuid.uuid4()),
        "imdb_rating": 8.5,
        "genres": [
            {"id": "123", "name": "Action"},
            {"id": "124", "name": "Sci-Fi"},
        ],
        "title": "The Star",
        "description": "New World",
        "directors": [
            {"id": "321", "name": "Stan"},
        ],
        "actors_names": ["Ann", "Bob"],
        "writers_names": ["Ben", "Howard"],
        "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
        "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat(),
        "type": "movie",
    }
    return film
