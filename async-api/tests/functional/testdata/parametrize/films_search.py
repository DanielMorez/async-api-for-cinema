films_search = [
    ({"query": "The Star"}, {"status": 200, "length": 50}),
    ({"query": "Mashed potato"}, {"status": 200, "length": 0}),
]

cache_search_films = [
    (
        None,
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.films:search_film:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': FilmQueryParams(page_size=50, page_number=0, sort='imdb_rating:desc', query=None)}\"}",
        },
    )
]

persons_search = [
    ({"query": "Rafael Ferrer"}, {"status": 200, "length": 1}),
    ({"query": "Mashed potato"}, {"status": 200, "length": 0}),
]


cache_search_persons = [
    (
        None,
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.persons:person_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': PersonSearchParams(page_size=50, page_number=0, query=None)}\"}",
        },
    ),
]
