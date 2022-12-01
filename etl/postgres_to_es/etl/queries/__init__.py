from etl.queries.genres import QUERY_TO_GET_LAST_MODIFIED_GENRES
from etl.queries.movies import QUERY_TO_GET_LAST_MODIFIED
from etl.queries.persons import QUERY_TO_GET_LAST_MODIFIED_PERSONS

QUERIES = {
    'movies': QUERY_TO_GET_LAST_MODIFIED,
    'persons': QUERY_TO_GET_LAST_MODIFIED_PERSONS,
    'genres': QUERY_TO_GET_LAST_MODIFIED_GENRES,
}
