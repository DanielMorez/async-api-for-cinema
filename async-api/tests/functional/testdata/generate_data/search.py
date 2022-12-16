import uuid

from elastic_transport import ObjectApiResponse


def generate_search_film(amount: int = 1):
    es_data = [{
        'id': str(uuid.uuid4()),
        'imdb_rating': 8.5,
        'title': 'The Star',
        'description': 'New World',
        'genres': [
            {'id': '111111', 'name': 'Action'},
            {'id': '222222', 'name': 'Sci-Fi'}
        ],

        'directors_names': ['Stan'],
        'actors_names': ['Ann', 'Bob'],
        'writers_names': ['Ben', 'Howard'],
        'directors': [
            {'id': '1111', 'name': 'Stan'}
        ],
        'actors': [
            {'id': '111', 'name': 'Ann'},
            {'id': '222', 'name': 'Bob'}
        ],
        'writers': [
            {'id': '333', 'name': 'Ben'},
            {'id': '444', 'name': 'Howard'}
        ],
        'type': 'movie'
    } for _ in range(amount)]
    return es_data


def extract_es_index(es_data: ObjectApiResponse):
    search_list = []
    rows = es_data["hits"]["hits"]
    for row in rows:
        cash_dict = row["_source"]
        cash_dict["id"] = row["_id"]
        search_list.append(cash_dict)
    return search_list
