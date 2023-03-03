import uuid

from api.v1.film_views.models import Frame
from fastapi import APIRouter, Depends, Request
from fastapi.security import HTTPBearer
from fastapi_contrib.auth.permissions import IsAuthenticated
from fastapi_contrib.permissions import PermissionsDependency
from fastapi_utils.cbv import cbv
from services.broker import BaseBrokerService, get_broker_service

from auth.models import User

router = APIRouter(
    prefix="/film-views",
    tags=["film views"],
    dependencies=[
        Depends(HTTPBearer()),
        Depends(PermissionsDependency([IsAuthenticated])),
    ],
)


@cbv(router)
class FrameCBV:
    service: BaseBrokerService = Depends(get_broker_service)

    @router.post(
        "/{film_id}",
        description="Fixing the reviewed frame",
        tags=["film views"],
        response_model=Frame,
    )
    async def viewed_frame(
        self, request: Request, film_id: uuid.UUID, timestamp: int
    ) -> Frame:
        user: User = request.user
        message = {
            "user_id": user.identity,
            "film_id": str(film_id),
            "timestamp": timestamp,
        }
        key = f"{user.identity}:{film_id}"
        await self.service.send_message(key, message)
        return Frame(user_id=user.identity, film_id=film_id, timestamp=timestamp)
