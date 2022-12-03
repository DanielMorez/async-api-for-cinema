from etl.extractors.genres import GenreExtractor
from etl.extractors.movies import FilmworkExtractor
from etl.extractors.persons import PersonExtractor

EXTRACTORS = {
    'movies': FilmworkExtractor,
    'persons': PersonExtractor,
    'genres': GenreExtractor,
}