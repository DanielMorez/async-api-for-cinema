from models.person import Person


def convert_person_for_es(persons: list[Person], index: str) -> list[dict]:
    actions = [
        {
            "_index": index,
            "_id": person.id,
            "_source": {
            }
        } for person in persons
    ]
    return actions
