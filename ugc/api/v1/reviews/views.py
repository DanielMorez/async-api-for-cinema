from uuid import UUID

from fastapi import APIRouter, Depends, Request, Query
from fastapi.security import HTTPBearer
from fastapi_utils.cbv import cbv
from fastapi_contrib.auth.permissions import IsAuthenticated
from fastapi_contrib.permissions import PermissionsDependency

from api.v1.reviews.models import Review
from auth.models import User
from services.mongo import MongoService
from services.service import get_service

router = APIRouter(
    prefix="/reviews",
    tags=["reviews"],
    dependencies=[
        Depends(HTTPBearer()),
        Depends(PermissionsDependency([IsAuthenticated])),
    ],
)


@cbv(router)
class ReviewsAPIView:
    service: MongoService = Depends(get_service)

    @router.post(
        "/{film_id}",
        description="Review a film"
    )
    async def review_film(
        self, request: Request, film_id: UUID, text: str = Query(max_length=100)
    ) -> str:
        user: User = request.user
        inserted_id = await self.service.add_review(film_id, user.id, text)
        return inserted_id

    @router.get(
        "/{film_id}",
        description="Get film reviews",
        response_model=list[Review]
    )
    async def film_reviews(self, film_id: UUID) -> list[dict]:
        response = await self.service.reviews(film_id)
        return response

    @router.delete(
        "/{film_id}",
        description="Delete film reviews"
    )
    async def delete_film_review(self, film_id: UUID) -> None:
        response = await self.service.remove_review(film_id)
        return response

    @router.post(
        "/{film_id}/like",
        description="Like a film review"
    )
    async def like_film_review(self, request: Request, review_id: str) -> None:
        response = await self.service.like_review(review_id, request.user.id)
        return response

    @router.post(
        "/{film_id}/dislike",
        description="Dislike a film review"
    )
    async def dislike_film_review(self, request: Request, review_id: str) -> None:
        response = await self.service.dislike_review(review_id, request.user.id)
        return response
