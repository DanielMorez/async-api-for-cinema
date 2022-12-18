import uuid

from elastic_transport import ObjectApiResponse


def generate_search_films(amount: int = 1) -> list:
    es_data = [
        {
            "id": str(uuid.uuid4()),
            "imdb_rating": 8.5,
            "title": "The Star",
            "description": "New World",
            "genres_": [
                {"id": "111111", "name": "Action"},
                {"id": "222222", "name": "Sci-Fi"},
            ],
            "directors_names": ["Stan"],
            "actors_names": ["Ann", "Bob"],
            "writers_names": ["Ben", "Howard"],
            "directors": [{"id": "1111", "name": "Stan"}],
            "actors": [{"id": "111", "name": "Ann"}, {"id": "222", "name": "Bob"}],
            "writers": [{"id": "333", "name": "Ben"}, {"id": "444", "name": "Howard"}],
            "type": "movie",
        }
        for _ in range(amount)
    ]
    return es_data


def extract_es_index(es_data: ObjectApiResponse):
    search_list = []
    rows = es_data["hits"]["hits"]
    for row in rows:
        cash_dict = row["_source"]
        cash_dict["id"] = row["_id"]
        search_list.append(cash_dict)
    return search_list


def generate_persons_films() -> list:
    es_data = [
        {
            "id": "578593ee-3268-4cd4-b910-8a44cfd05b73",
            "name": "Rafael Ferrer",
            "gender": "male",
            "roles_names": ["actor"],
            "films_names": ["NeverLand"],
            "films": [
                {"id": "2a090dde-f688-46fe-a9f4-b781a985275e", "title": "NeverLand"}
            ],
        },
        {
            "id": "2802ff93-f147-49cc-a38b-2f787bd2b875",
            "name": "John Cygan",
            "gender": "male",
            "roles_names": ["actor"],
            "films_names": ["Movie 43", "NeverLand"],
            "films": [
                {"id": "64aa7000-698f-4332-b52f-9469e4d44ee1", "title": "Movie 43"},
                {"id": "2a090dde-f688-46fe-a9f4-b781a985275e", "title": "NeverLand"},
            ],
        },
        {
            "id": "c740cb33-df3a-4aeb-b3ad-7e79581d857c",
            "name": "Fabio Rinaudo",
            "gender": "female",
            "roles_names": ["actor", "producer"],
            "films_names": ["The Star", "NeverLand"],
            "films": [
                {"id": "7159c8c2-b9a4-410a-965b-1096b8d1e614", "title": "The Star"},
                {"id": "2a090dde-f688-46fe-a9f4-b781a985275e", "title": "NeverLand"},
            ],
        },
        {
            "id": "f142081a-8054-4ec3-ae97-026f8ebdef3e",
            "name": "Tiziana Lodato",
            "gender": None,
            "roles_names": ["actor"],
            "films_names": ["The Star"],
            "films": [
                {"id": "7159c8c2-b9a4-410a-965b-1096b8d1e614", "title": "The Star"}
            ],
        },
        {
            "id": "a88f14e6-a8e2-4e05-9744-e89fadf960fb",
            "name": "Franco Scaldati",
            "gender": "male",
            "roles_names": ["actor"],
            "films_names": ["The Star"],
            "films": [
                {"id": "7159c8c2-b9a4-410a-965b-1096b8d1e614", "title": "The Star"}
            ],
        },
        {
            "id": "6d5964ff-e56e-40aa-9e30-6a52ed741e55",
            "name": "Leopoldo Trieste",
            "gender": "male",
            "roles_names": ["actor"],
            "films_names": ["The Star"],
            "films": [
                {"id": "7159c8c2-b9a4-410a-965b-1096b8d1e614", "title": "The Star"}
            ],
        },
        {
            "id": "8fadd3bf-c272-4b84-be93-0f85f0a0767e",
            "name": "Ry Russo-Young",
            "gender": None,
            "roles_names": ["director"],
            "films_names": ["Wonderland"],
            "films": [
                {"id": "523f1a55-51fe-4d3c-a58d-30d8a61bb267", "title": "Wonderland"}
            ],
        },
    ]
    return es_data
