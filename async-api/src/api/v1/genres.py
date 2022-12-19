from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from fastapi_utils.cbv import cbv

from api.v1.queries_params.genres import GenreListParams
from helpers.detail_messages import DETAILS
from models import Genre
from services.genre import GenreService, get_genre_service

router = APIRouter()


@cbv(router)
class GenreCBV:
    service: GenreService = Depends(get_genre_service)
    response_model = Genre

    @router.get(
        "/",
        description="Get the list of genres",
        summary="The list of genres",
        response_description="The list of genres",
        tags=["genres"],
    )
    @cache()
    async def genre_list(self, params: GenreListParams = Depends()) -> list[Genre]:
        """
        Returns list of genres sorted by name: desc (default value).
        """
        genres = await self.service.get_list(params)
        return genres

    @router.get(
        "/{genre_id}",
        description="Get genre's data by id",
        summary="Genre's data",
        response_description="Genre's data",
        tags=["genres"],
    )
    @cache()
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
