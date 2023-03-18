from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, Body
from fastapi_utils.cbv import cbv

from api.models import Notification
from services.rabbitmq import BrokerRabbitMQService
from services.service import get_broker_service

router = APIRouter(
    tags=["notifications"]
)


@cbv(router)
class NotificationAPIView:
    broker: BrokerRabbitMQService = Depends(get_broker_service)

    @router.post(
        "/send",
        description="Send any notifications",
        status_code=HTTPStatus.CREATED
    )
    async def send_notification(self, payload: Notification) -> None:
        await self.broker.send_message(payload.dict())

    @router.post(
        "/registration",
        description="Send register email",
        status_code=HTTPStatus.CREATED
    )
    async def send_register_email(self, user_id: UUID = Body()) -> None:
        payload = Notification(
            type="personal",
            template_id=1,  # set actual template id
            user_ids=[user_id],
            context={}
        )
        await self.broker.send_message(payload.dict())
