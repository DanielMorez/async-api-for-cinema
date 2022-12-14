film_list_params = [
    (None, {"status": 200, "length": 50}),
    ({"page[size]": 10}, {"status": 200, "length": 10}),
    ({"page[size]": 60}, {"status": 200, "length": 60}),
]

cache_film_list_params = [
    (
        None,
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.films:film_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': FilmListParams(page_size=50, page_number=0, sort='imdb_rating:desc', genre_id=None)}\"}",
        },
    ),
    (
        {"page[size]": 10},
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.films:film_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': FilmListParams(page_size=10, page_number=0, sort='imdb_rating:desc', genre_id=None)}\"}",
        },
    ),
    (
        {"page[size]": 60},
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.films:film_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': FilmListParams(page_size=60, page_number=0, sort='imdb_rating:desc', genre_id=None)}\"}",
        },
    ),
]
