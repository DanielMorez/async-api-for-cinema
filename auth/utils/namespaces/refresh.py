from flask_restx import Namespace

ns = Namespace(
    "Refresh tokens",
    description="Here the user can exchange a refresh token for a pair of new tokens: access and refresh",
)
