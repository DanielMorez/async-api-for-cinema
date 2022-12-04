from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache import JsonCoder
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.genres import GenreListParams
from helpers.cache_key_builder import CACHE_EXPIRE_IN_SECONDS, key_builder
from helpers.detail_messages import DETAILS
from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@cbv(router)
class GenreCBV:
    service: GenreService = Depends(get_genre_service)
    response_model = Genre

    @router.get("/")
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def genre_list(self, params: GenreListParams = Depends()) -> list[Genre]:
        """
        Returns list of genres sorted by name: desc (default value).
        """
        genres = await self.service.get_list(params)
        return genres

    @router.get("/{genre_id}")
    @cache(expire=CACHE_EXPIRE_IN_SECONDS, coder=JsonCoder, key_builder=key_builder)
    async def genre_details(self, genre_id: str) -> Genre:
        """
        Returns the dict with all information about the genre by ID.
        """
        genre = await self.service.get_by_id(genre_id)
        if not genre:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND, detail=DETAILS["not_found"]
            )
        return genre
