import logging
from http import HTTPStatus

import click
from flask import Blueprint

from db import db
from models.user import User
from models.role import UserRoles, Role

bp = Blueprint("superuser", __name__)

logger = logging.getLogger(__name__)

@bp.cli.command("create")
@click.argument("login")
@click.argument("password")
@click.argument("password_confirm")
@click.argument("email")
# TODO add role, user_role
def createsuperuser(login, password, password_confirm, email=None):
    user_exist = db.session.query(User).filter(User.login == login).first()
    if user_exist:
        print("User already exists. Try another login")
        return {"message": f"User with login {login} already exists"}, HTTPStatus.RESET_CONTENT
    if password_confirm == password:
        try:
            superuser = User(login=login, password=password, email=email, is_superuser=True)
            superuser.save()
            role = Role(name="Admin", can_create_update=True, can_read=True, can_delete=True)
            role.save()
            new_role_user = UserRoles(user_id=superuser.id, role_id=role.id)
            new_role_user.save()
        except Exception as error:
            logger.error(error)
            return {"message": "Something went wrong"}, HTTPStatus.INTERNAL_SERVER_ERROR
    else:
        print("Password and Password_confirm don't match. Try again")
        return {"message": "Password and Password_confirm don't match"}, HTTPStatus.BAD_REQUEST
    print("Superuser is created successfully")
    return {"message": "Superuser is created successfully"}, HTTPStatus.CREATED
