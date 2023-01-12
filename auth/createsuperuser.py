import click
from flask import Blueprint

from db import db
from models import User

bp = Blueprint("superuser", __name__)


@bp.cli.command("create")
@click.argument("login")
@click.argument("password")
@click.argument("password_confirm")
@click.argument("email")
# TODO add role, user_role
def createsuperuser(login, password, password_confirm, email=None):
    user_exist = db.session.query(User).filter(User.login == login).first()
    if user_exist:
        return "User already exist. Try another login"
    if password_confirm == password:
        superuser = User(login=login, password=password, email=email)
        superuser.save()
    else:
        return "Password and Password_confirm are different. Try again"
    return "Superuser was created"
