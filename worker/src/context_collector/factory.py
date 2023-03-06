from user_service_client.client_abstract import UserServiceClientAbstract

from .abstract import ContextCollectorAbstract
from .monthly_personal_statistic import ContextCollectorMonthlyPersonalStatistic


class NotFoundException(Exception):
    """Context collector not found."""


class ContextCollectorFactory():
    def __init__(self, user_service_client: UserServiceClientAbstract):
        self.user_service_client = user_service_client

    def create(self, context_type: str) -> ContextCollectorAbstract:
        if context_type == 'monthly_personal_statistic':
            return ContextCollectorMonthlyPersonalStatistic(self.user_service_client)
        else:
            raise NotFoundException(f'Context collector for {context_type} not found')
