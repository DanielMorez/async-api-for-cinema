from http import HTTPStatus

from flask import redirect
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required
from flask_restful import Resource

from resources.parsers.auth import auth_parser, register_parser
from services.social_account_service import SocialAccountService
from services.user_service import JWTs, UserService
from utils.namespaces import login, login_google, logout, refresh, registration
from utils.namespaces.login import tokens
from utils.parsers.auth import access_token_required, refresh_token_required
from utils.parsers.login import credentials
from utils.parsers.registration import register_data
from utils.token import check_if_token_in_blacklist


@login_google.ns.route("")
class LoginWithGoogle(Resource):
    def get(self):
        redirect_uri = SocialAccountService.get_redirect_uri()
        return redirect(redirect_uri)


class LoginGoogleCallback(Resource):
    def get(self):
        token_response = SocialAccountService.get_google_token_access()
        social_account, account_data = SocialAccountService.get_social_account_data(token_response)

        if not social_account:
            payload, status = SocialAccountService.create_user(account_data)
        else:
            payload, status = SocialAccountService.current_user_login(social_account)

        return payload, status


@registration.ns.route("")
@registration.ns.expect(register_data)
class Registration(Resource):
    @registration.ns.marshal_with(tokens, code=HTTPStatus.CREATED)
    def post(self):
        """Register user"""
        data = register_parser.parse_args()
        payload, status = UserService.register(**data)
        return payload, status


@login.ns.route("")
@login.ns.expect(credentials)
class Authorization(Resource):
    @login.ns.marshal_with(tokens)
    def post(self):
        """Authorization by credentials"""
        data = auth_parser.parse_args()
        payload, status = UserService.login(data["login"], data["password"], data.get("User-Agent"), data.get("Device"))
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            return payload.dict(), status
        return payload, status


@refresh.ns.route("")
@refresh.ns.expect(refresh_token_required)
class RefreshToken(Resource):
    @refresh.ns.marshal_with(tokens)
    @jwt_required(refresh=True)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        refresh_token = get_jwt()
        payload, status = UserService.refresh(user_id, refresh_token)
        if status == HTTPStatus.OK and isinstance(payload, JWTs):
            return payload.dict(), status
        return payload, status


@logout.ns.route("")
@logout.ns.expect(access_token_required)
class Logout(Resource):
    @jwt_required(verify_type=False)
    @check_if_token_in_blacklist()
    def post(self):
        user_id = get_jwt_identity()
        payload = get_jwt()
        payload, status = UserService.logout(user_id, payload)
        return payload, status
