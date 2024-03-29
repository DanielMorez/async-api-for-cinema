from flask import Blueprint
from flask_restful import Api
from flask_restx import Api as OpenAPI

from resources import auth, profile, login_history, role, user_role, user_ids, user_data

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/user")
auth_api = Api(auth_bp)
swagger = OpenAPI(
    auth_bp,
    description="This is the documentation for working with authorization service methods",
)

# route endpoints
auth_api.add_resource(auth.LoginWithGoogle, "/login-google")
auth_api.add_resource(auth.LoginGoogleCallback, "/login-google/callback")

auth_api.add_resource(auth.Registration, "/register")
auth_api.add_resource(auth.Authorization, "/login")
auth_api.add_resource(auth.Logout, "/logout")
auth_api.add_resource(auth.RefreshToken, "/token-refresh")

auth_api.add_resource(profile.Profile, "/profile")
auth_api.add_resource(profile.ChangePassword, "/profile/change-password")
auth_api.add_resource(profile.ChangeLogin, "/profile/change-login")

auth_api.add_resource(login_history.LoginHistories, "/login-histories")

auth_api.add_resource(role.RoleResource, "/roles")
auth_api.add_resource(user_role.UserRoleResource, "/user-role")

auth_api.add_resource(user_ids.UserIds, "/user-ids")
auth_api.add_resource(user_data.UserPersonalData, "/user-data")

# openapi
swagger.add_namespace(auth.registration.ns, "/register")
swagger.add_namespace(auth.login.ns, "/login")
swagger.add_namespace(auth.login_google.ns, "/login-google")
swagger.add_namespace(auth.logout.ns, "/logout")
swagger.add_namespace(auth.refresh.ns, "/token-refresh")

swagger.add_namespace(profile.ns, "/profile")
swagger.add_namespace(login_history.ns, "/login-histories")

swagger.add_namespace(role.ns, "/roles")
swagger.add_namespace(user_role.ns, "/user-role")

swagger.add_namespace(user_ids.ns, "/user-ids")
swagger.add_namespace(user_data.ns, "/user-data")
