from datetime import datetime
from uuid import UUID

from api.v1.rating.models import PydanticObjectId
from core.utils import orjson_dumps
from orjson import orjson
from pydantic import BaseModel, Field


class Review(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    user_id: UUID
    film_id: UUID
    text: str
    created_at: datetime = Field(default_factory=datetime.now)
    likes: int = Field(0)
    dislikes: int = Field(0)

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class UserFilmRating(BaseModel):
    id: PydanticObjectId = Field(None, alias="_id")
    film_id: UUID
    stars_avg: float = Field(None, ge=0, le=10)
    count: int = Field(0)
    stars: int = Field(None)

    class Config:
        arbitrary_types_allowed = True
        json_loads = orjson.loads
        json_dumps = orjson_dumps


class ReviewLike(BaseModel):
    review_id: str
    user_id: UUID
    type: str = Field(regex=r"(like|dislike)")
