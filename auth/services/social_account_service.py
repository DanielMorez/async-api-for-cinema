import jwt
import json
import string
import requests

from http import HTTPStatus
from secrets import choice as secrets_choice

from flask import abort, request, Response
from flask_jwt_extended import create_access_token, create_refresh_token

from config import settings, client
from models.social_account import SocialAccount
from services.user_service import UserService, JWTs


def generate_random_string():
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets_choice(alphabet) for _ in range(16))


class SocialAccountService:
    google_discovery_url = settings.GOOGLE_DISCOVERY_URL

    @classmethod
    def get_tokens(cls, social_account: SocialAccount) -> JWTs:
        return JWTs(
            access_token=create_access_token(identity=social_account.user_id),
            refresh_token=create_refresh_token(identity=social_account.user_id),
        )

    @classmethod
    def google_provider(cls) -> dict:
        return requests.get(cls.google_discovery_url).json()

    @classmethod
    def get_redirect_uri(cls) -> str:
        google_provider_cfg = cls.google_provider()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )
        return request_uri

    @classmethod
    def get_google_token_access(cls) -> Response:
        code = request.args.get("code")
        google_provider_cfg = cls.google_provider()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code,
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(settings.GOOGLE_CLIENT_ID, settings.GOOGLE_CLIENT_SECRET),
        )
        return token_response

    @classmethod
    def get_social_account_data(cls, token_response: Response) -> (SocialAccount, dict):
        client.parse_request_body_response(json.dumps(token_response.json()))
        google_provider_cfg = cls.google_provider()

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            social_id = userinfo_response.json()["sub"]

            account_data = {
                "login": userinfo_response.json()["name"],
                "user_name": userinfo_response.json()["name"],
                "email": userinfo_response.json()["email"],
                "first_name": userinfo_response.json()["given_name"],
                "last_name": userinfo_response.json()["family_name"],
                "social_id": social_id,
            }
            social_account = SocialAccount.find_by_id(social_id=social_id)
            return social_account, account_data
        else:
            abort(
                HTTPStatus.BAD_REQUEST,
                "User email not available or not verified by Google",
            )

    @classmethod
    def create_user(cls, account_data) -> (dict, HTTPStatus):
        password = generate_random_string()
        account_data["password"] = password
        account_data["password_confirmation"] = password
        payload, status = UserService.register(**account_data)
        user_id = jwt.decode(
            payload["access_token"], options={"verify_signature": False}
        )["sub"]
        if status == HTTPStatus.CREATED:
            social_account = SocialAccount(
                user_id=user_id,
                social_id=account_data["social_id"],
                social_name=account_data["user_name"],
            )
            social_account.save()
            payload[
                "password"
            ] = password
            # TODO: send the password to the user's email and a message about the need to update the password
            return payload, status
        else:
            abort(HTTPStatus.BAD_REQUEST, "User already exists")

    @classmethod
    def current_user_login(cls, social_account) -> (dict, HTTPStatus):
        tokens: JWTs = SocialAccountService.get_tokens(social_account)
        return tokens.dict(), HTTPStatus.OK
