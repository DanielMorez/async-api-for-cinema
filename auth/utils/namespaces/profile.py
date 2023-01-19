from flask_restx import Namespace, fields

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
        "login": fields.String(),
        "first_name": fields.String(),
        "last_name": fields.String(),
        "email": fields.String(),
    },
)
