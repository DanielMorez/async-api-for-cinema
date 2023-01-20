from flask_restx import Namespace, fields
from flask_restx import reqparse

ns = Namespace("Roles", description="CRUD for role management")

role = ns.model(
    "Role",
    {
        "id": fields.String(readonly=True, description="The role UUID identifier"),
        "name": fields.String(required=True, description="The role name"),
    },
)

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, location="json")

role_id = reqparse.RequestParser()
role_id.add_argument("id", type=str, required=True, location="json")
