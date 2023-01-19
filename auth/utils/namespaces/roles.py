from flask_restx import Namespace, fields, Model

ns = Namespace("Roles", description="CRUD for role management")

role = ns.model(
    "Role",
    {
        "id": fields.String(readonly=True, description="The role UUID identifier"),
        "name": fields.String(required=True, description="The role name"),
    },
)
