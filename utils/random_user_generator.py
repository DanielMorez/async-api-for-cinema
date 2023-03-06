"""Утилита для генерации json с рандомными юзерами."""

import json
import random
import uuid

import requests as requests
from pydantic.main import BaseModel


class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    promo_agree: bool
    category: str
    films_month_count: int
    favourite_genre: str


def generate_user() -> UserInfo:
    response = requests.get('https://randomuser.me/api/?nat=us')
    data = response.json()

    genres = ['аниме', 'биографический', 'боевик', 'вестерн', 'военный', 'детектив', 'детский', 'документальный']

    return UserInfo(
        id=str(uuid.uuid4()),
        first_name=data['results'][0]['name']['first'],
        last_name=data['results'][0]['name']['last'],
        email=data['results'][0]['email'],
        promo_agree=bool(random.getrandbits(1)),
        category='active' if random.randrange(10) < 9 else 'inactive',
        films_month_count=random.randrange(15),
        favourite_genre=random.choice(genres)
    )


def main():
    users = []
    for _ in range(100):
        user = generate_user()
        users.append(user.dict())
        print(user)

    with open('users.json', 'w') as file:
        json.dump({'users': users}, file)


if __name__ == '__main__':
    main()
