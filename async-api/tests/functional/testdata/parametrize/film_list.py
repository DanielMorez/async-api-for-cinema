film_list_params = [
    (
        None,
        {'status': 200, 'length': 50}
    ),
    (
        {'page[size]': 10},
        {'status': 200, 'length': 10}
    ),
    (
        {'page[size]': 60},
        {'status': 200, 'length': 60}
    ),
]
