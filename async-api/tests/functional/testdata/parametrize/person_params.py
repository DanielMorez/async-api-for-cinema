params = [
    (
        {"query": "Rafael Ferrer"},
        {"status": 200, "length": 1}
    ),
    (
        {"query": "Mashed potato"},
        {"status": 200, "length": 0}
    )
]
not_found_id = [
    (
        {"name": "Rafael Ferrer"},
        {"status": 200, "length": 1}
    ),
    (
        {"query": "Mashed potato"},
        {"status": 200, "length": 0}
    ),
    (
        {"id": "www-www-www"},
        {"status": 404, "length": 0}
    )
]