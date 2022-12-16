import uuid


def generate_persons(amount: int = 60) -> list[dict]:
    persons = [generate_person() for i in range(amount)]
    return persons


def generate_person() -> dict:
    person = {
        'id': str(uuid.uuid4()),
        'name': 'Rafael Ferrer',
        'gender': 'male',
        'roles_names': ['director', 'writer'],
        'films_names': ['Casper', 'Kolombiana', 'Star Dust'],
        'films': [
            {'id': '111', 'title': 'Casper'},
            {'id': '222', 'title': 'Kolombiana'},
            {'id': '333', 'title': 'Star Dust'}
        ],
    }
    return person
