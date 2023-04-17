from uuid import UUID

from django.conf import settings
from requests import post, delete
from rest_framework import status


class AuthClient:
    def __init__(self, dsn: str):
        self.dsn = dsn

    def assign_subscriber_role(self, user_id: UUID):
        response = post(
            self.dsn + "/api/v1/user/user-role",
            json={"user_id": str(user_id), "role_id": settings.SUBSCRIBER_ROLE_ID}
        )
        return response.status_code == status.HTTP_200_OK

    def remove_subscriber_role(self, user_id: UUID):
        response = delete(
            self.dsn + "/api/v1/user/user-role",
            json={"user_id": str(user_id), "role_id": settings.SUBSCRIBER_ROLE_ID}
        )
        return response.status_code == status.HTTP_200_OK
