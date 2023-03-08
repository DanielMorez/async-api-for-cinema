from uuid import UUID

from fastapi import APIRouter, Depends, Request, Body
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
        "/",
        description="Review a film"
    )
    async def review_film(
        self, request: Request, film_id: UUID = Body(), text: str = Body(max_length=100)
    ) -> str:
        user: User = request.user
        inserted_id = await self.service.add_review(film_id, user.id, text)
        return inserted_id

    @router.get(
        "/",
        description="Get film reviews",
        response_model=list[Review]
    )
    async def film_reviews(self, film_id: UUID = Body()) -> list[dict]:
        response = await self.service.reviews(film_id)
        return response

    @router.delete(
        "/",
        description="Delete film reviews"
    )
    async def delete_film_review(self, request: Request, review_id: str = Body()) -> None:
        response = await self.service.remove_review(review_id, request.user.id)
        return response

    @router.post(
        "/like",
        description="Like a film review"
    )
    async def like_film_review(self, request: Request, review_id: str = Body()) -> None:
        response = await self.service.like_review(review_id, request.user.id)
        return response

    @router.post(
        "/dislike",
        description="Dislike a film review"
    )
    async def dislike_film_review(self, request: Request, review_id: str) -> None:
        response = await self.service.dislike_review(review_id, request.user.id)
        return response
