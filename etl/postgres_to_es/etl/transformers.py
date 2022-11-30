from models import Movie


def convert_movies_for_es(movies: list[Movie], index: str) -> list[dict]:
    actions = [
        {
            "_index": index,
            "_id": movie.id,
            "_source": {
                "title": movie.title,
                "genres": [genre.dict() for genre in movie.genres],
                "genres_names": [genre.name for genre in movie.genres],
                "imdb_rating": movie.rating,
                "description": movie.description,
                "actors": [person.dict() for person in movie.actors],
                "actors_names": [person.name for person in movie.actors],
                "writers": [person.dict() for person in movie.writers],
                "writers_names": [person.name for person in movie.writers],
                "directors": [person.dict() for person in movie.directors],
                "directors_names": [person.name for person in movie.directors],
            }
        } for movie in movies
    ]
    return actions
