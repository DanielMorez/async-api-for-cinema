from flask_restx import Namespace, fields

ns = Namespace(
    "Login histories",
    description="Here the user can get information about his authorizations",
)

login_history = ns.model(
    "Login History",
    {
        "id": fields.String(readonly=True, description="The login history UUID identifier"),
        "user_agent": fields.String(),
        "device": fields.String(),
        "created_at": fields.DateTime()
    }
)