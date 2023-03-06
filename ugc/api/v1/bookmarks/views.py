from uuid import UUID

from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_utils.cbv import cbv
from fastapi_contrib.auth.permissions import IsAuthenticated
from fastapi_contrib.permissions import PermissionsDependency

from api.v1.bookmarks.models import Bookmark
from auth.models import User
from services.mongo import MongoService
from services.service import get_service

router = APIRouter(
    prefix="/bookmarks",
    tags=["movie bookmarks"],
    dependencies=[
        Depends(HTTPBearer()),
        Depends(PermissionsDependency([IsAuthenticated])),
    ],
)


@cbv(router)
class BookmarkAPIView:
    service: MongoService = Depends(get_service)

    @router.post(
        "/{film_id}",
        description="Add movie to user bookmarks",
        tags=["movie bookmarks"],
        response_model=Bookmark
    )
    async def create_bookmark(
        self, request: Request, film_id: UUID
    ) -> dict:
        user: User = request.user
        response = await self.service.add_bookmark(user.id, film_id)
        return response

    @router.get(
        "/list",
        description="Get user bookmarks",
        tags=["movie bookmarks"],
        response_model=list[Bookmark]
    )
    async def user_bookmarks(self, request: Request) -> list[dict]:
        user: User = request.user
        response = await self.service.user_bookmarks(user.id)
        return response

    @router.delete(
        "/{bookmark_id}",
        description="Delete user bookmarks",
        tags=["movie bookmarks"]
    )
    async def remove_bookmark(self, request: Request, bookmark_id: UUID) -> None:
        user: User = request.user
        await self.service.remove_bookmark(user_id=user.id, bookmark_id=bookmark_id)
