from flask_restx import Namespace, fields
from flask_restx import reqparse

ns = Namespace(
    "Profile",
    description="Here the user can get information about his profile and change it",
)
user = ns.model(
    "User",
    {
        "id": fields.String(
            readonly=True, description="The login history UUID identifier"
        ),
        "login": fields.String(readonly=True),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
    },
)

login = reqparse.RequestParser()
login.add_argument("login", type=str, required=True, location="json")

password = reqparse.RequestParser()
password.add_argument("password", type=str, required=True, location="json")
