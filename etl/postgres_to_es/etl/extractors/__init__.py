from etl.extractors.movies import FilmworkExtractor
from etl.extractors.persons import PersonExtractor

EXTRACTORS = {
    'movies': FilmworkExtractor,
    'persons': PersonExtractor
}