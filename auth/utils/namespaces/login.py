from flask_restx import Namespace, fields


ns = Namespace("Login", description="Here the user can authorization")


tokens = ns.model(
    "Tokens",
    {
        "access_token": fields.String(readonly=True),
        "refresh_token": fields.String(readonly=True),
    },
)
