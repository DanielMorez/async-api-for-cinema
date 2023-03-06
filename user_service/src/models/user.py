import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    return orjson.dumps(v, default=default).decode()


class UserInfo(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: str
    promo_agree: bool
    category: str
    films_month_count: int
    favourite_genre: str
