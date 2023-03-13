from services.base_service import BaseBrokerService


class BrokerRabbitMQService(BaseBrokerService):
    async def send_message(self, message: dict) -> None:
        await self._producer.send(message)
