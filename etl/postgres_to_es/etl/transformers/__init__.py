from etl.transformers.movies import convert_movies_for_es
from etl.transformers.persons import convert_person_for_es

TRANSFORMERS = {
    'movies': convert_movies_for_es,
    'persons': convert_person_for_es
}