import uuid


def generate_genres(amount: int = 60) -> list[dict]:
    genres = [generate_genre() for i in range(amount)]
    return genres


def generate_genre() -> dict:
    genre = {
        "id": str(uuid.uuid4()),
        "name": "Drama",
    }
    return genre
