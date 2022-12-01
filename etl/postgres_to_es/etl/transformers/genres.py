from models.genre import Genre


def convert_genre_for_es(genres: list[Genre], index: str) -> list[dict]:
    actions = [
        {
            "_index": index,
            "_id": genre.id,
            "_source": {
                "name": genre.name,
                "description": genre.description,
            }
        } for genre in genres
    ]
    return actions
