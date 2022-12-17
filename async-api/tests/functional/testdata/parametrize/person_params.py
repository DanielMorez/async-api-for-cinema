person_list_params = [
    (None, {"status": 200, "length": 30}),
    ({"page[size]": 10}, {"status": 200, "length": 10}),
    ({"page[size]": 30}, {"status": 200, "length": 30}),
]

cache_person_list_params = [
    (
        None,
        {
            "status": 200,
            "key": "fastapi-cache:api.v1.persons:person_list:('',):{'request': None, 'response': None, 'args': (), 'kwargs': \"{'self': <>, 'params': PersonSearchParams(page_size=50, page_number=0, query=None)}\"}"
        },
    ),
]