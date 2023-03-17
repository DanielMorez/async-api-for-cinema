import uuid

from flask_restx import Namespace, reqparse, fields

ns = Namespace("User personal data", description="Using by notification service (worker)")

user_ids_model = ns.model(
    "User IDs",
    {
        "user_ids": fields.List(
            fields.String(), required=True, default=[str(uuid.uuid4())]
        )
    }
)

user_ids = reqparse.RequestParser()
user_ids.add_argument("user_ids", type=list, required=True, location="json")
