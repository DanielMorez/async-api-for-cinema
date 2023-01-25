genre_list_params = [
    (None, {"status": 200, "length": 50}),
    ({"page[size]": 10}, {"status": 200, "length": 10}),
    ({"page[size]": 60}, {"status": 200, "length": 60}),
]

cache_genre_list_params = [
    (
        None,
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.genres:genre_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': GenreListParams(page_size=50, page_number=0, name=None, sort=None)}\"}"
        },
    ),
]