from typing import Any, Dict

from user_service_client.client_abstract import UserServiceClientAbstract

from .abstract import ContextCollectorAbstract


class ContextCollectorMonthlyPersonalStatistic(ContextCollectorAbstract):
    def __init__(self, user_service_client: UserServiceClientAbstract):
        self.user_service_client = user_service_client

    def collect(self, user_id: str) -> Dict[Any, Any]:
        """Return `films_month_count` and `favourite_genre` for user."""
        user = self.user_service_client.get_user(user_id)

        return user.dict(include={'films_month_count', 'favourite_genre'})
