import os

from authentication.client import AuthClient

AUTH_DSN = os.environ.get("AUTH_DSN")

AUTH_USER_MODEL = "authentication.User"

AUTH_CLIENT = AuthClient(AUTH_DSN)
SUBSCRIBER_ROLE_ID = os.environ.get("SUBSCRIBER_ROLE_ID")
