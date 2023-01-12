from flask import Blueprint
from flask_restful import Api

from resources import auth, profile, login_history

auth_bp = Blueprint("auth", __name__, url_prefix="/api/v1/user")
auth_api = Api(auth_bp)

# route endpoints
auth_api.add_resource(auth.Registration, "/register")
auth_api.add_resource(auth.Authorization, "/login")
auth_api.add_resource(auth.Logout, "/login")
auth_api.add_resource(auth.RefreshToken, "/token-refresh")

auth_api.add_resource(profile.Profile, "/profile")
auth_api.add_resource(profile.ChangePassword, "/change-password")
auth_api.add_resource(profile.ChangeLogin, "/change-login")

auth_api.add_resource(login_history.LoginHistories, "/login-histories")
