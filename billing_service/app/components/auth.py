import os

AUTH_DSN = os.environ.get("AUTH_DSN")

AUTH_USER_MODEL = "authentication.User"

AUTHENTICATION_BACKENDS = (
    "authentication.backends.AuthServiceBackend",
    "django.contrib.auth.backends.ModelBackend",
)
