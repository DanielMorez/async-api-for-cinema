from models.person import Person


def convert_person_for_es(persons: list[Person], index: str) -> list[dict]:
    actions = [
        {
            "_index": index,
            "_id": person.id,
            "_source": {
                "name": person.name,
                "gender": person.gender,
                "roles_names": person.roles,
                "films_names": [film.title for film in person.films],
                "films": [film.dict() for film in person.films],
            }
        } for person in persons
    ]
    return actions
