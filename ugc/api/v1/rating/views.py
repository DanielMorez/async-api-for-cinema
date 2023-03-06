from uuid import UUID

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPBearer
from fastapi_utils.cbv import cbv
from fastapi_contrib.auth.permissions import IsAuthenticated
from fastapi_contrib.permissions import PermissionsDependency

from api.v1.rating.models import Rate, UserFilmRating
from auth.models import User
from services.mongo import MongoService
from services.service import get_service

router = APIRouter(
    prefix="/rating",
    tags=["rating"],
    dependencies=[
        Depends(HTTPBearer()),
        Depends(PermissionsDependency([IsAuthenticated])),
    ],
)


@cbv(router)
class RatingAPIView:
    service: MongoService = Depends(get_service)

    @router.post(
        "/{film_id}",
        description="Rate a film (you can change rate everytime)"
    )
    async def rate_film(
        self, request: Request, film_id: UUID, stars: int = Query(ge=0, le=10)
    ) -> None:
        user: User = request.user
        await self.service.rate_film(film_id, user.id, stars)

    @router.get(
        "/{film_id}",
        description="Get user film rating",
        response_model=UserFilmRating
    )
    async def film_rating(self, film_id: UUID) -> UserFilmRating:
        response = await self.service.film_rating(film_id)
        return response
