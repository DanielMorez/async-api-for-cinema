from flask_restx import reqparse

access_token_required = reqparse.RequestParser()
access_token_required.add_argument(
    "Authorization",
    type=str,
    required=True,
    location="headers",
    help="Set access token. Token starts with Bearer.",
)

refresh_token_required = reqparse.RequestParser()
refresh_token_required.add_argument(
    "Authorization",
    type=str,
    required=True,
    location="headers",
    help="Set refresh token. Token starts with Bearer.",
)
