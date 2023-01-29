from flask_restx import Namespace, fields


ns = Namespace("Login by Google", description="Here the user can authorization by Google")


google_auth = ns.model(
    "Google Auth",
    {
        "redirect_uri": fields.String(readonly=True)
    },
)
