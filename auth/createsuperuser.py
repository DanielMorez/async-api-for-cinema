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
        print("User already exists. Try another login")
        return "Error 401 - User exists"
    if password_confirm == password:
        superuser = User(login=login, password=password, email=email)
        superuser.save()
    else:
        print("Password and Password_confirm don't match. Try again")
        return "Error 401 - Passwords don't match"
    print("Superuser is created successfully")
    return "200 OK"
