from http import HTTPStatus

from flask import abort
from flask_restful import reqparse


def validate_login(login):
    if len(login) <= 6:
        abort(
            HTTPStatus.BAD_REQUEST, "Login has to contains more pr equal 6 symbols"
        )
    return login


def validate_password(password):
    if len(password) <= 6:
        abort(
            HTTPStatus.BAD_REQUEST, "Password has to contains more pr equal 6 symbols"
        )
    return password


register_parser = reqparse.RequestParser()
register_parser.add_argument(
    "login", help="This field cannot be blank", required=True, type=validate_login
)
register_parser.add_argument(
    "password", help="This field cannot be blank", required=True, type=validate_password
)
register_parser.add_argument(
    "password_confirmation", help="This field cannot be blank", required=True
)
register_parser.add_argument("email", help="This field can be blank", required=False)

auth_parser = reqparse.RequestParser()
auth_parser.add_argument("login", help="This field cannot be blank", required=True)
auth_parser.add_argument("password", help="This field cannot be blank", required=True)
auth_parser.add_argument("User-Agent", location="headers")
auth_parser.add_argument("Device", location="headers")
