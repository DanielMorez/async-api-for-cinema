import requests

from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import status


class JWTAuthentication(BaseAuthentication):
    @staticmethod
    def authenticate(request, *args, **kwargs):
        User = get_user_model()

        auth_headers = request.headers.get("Authorization")

        if not auth_headers:
            return None

        response = requests.get(
            settings.AUTH_DSN + "/api/v1/user/profile",
            headers={"Authorization": auth_headers},
        )
        if response.status_code == status.HTTP_200_OK:
            data = response.json()
            if not User.objects.filter(id=data["id"]).exists():
                # We don't collect any personal data (also login), so using only id
                user = User(id=data["id"], username=data["id"])
                user.set_unusable_password()
                user.save()
            user = User(
                id=data["id"],
                username=data["login"],
                first_name=data["first_name"],
                last_name=data["last_name"],
                email=data["email"],
                roles=data.get("roles", []),
            )
            return user, None
