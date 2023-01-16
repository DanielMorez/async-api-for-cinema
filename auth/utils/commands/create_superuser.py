import click
import logging

from models import User

logger = logging.getLogger(__name__)


@click.command()
def test_command():
    print("HELLO WORLD!")


@click.command()
@click.argument("login")
@click.argument("password")
@click.argument("password_confirm")
def create_superuser(login, password, password_confirm, email=None):
    if User.find_by_login(login):
        print("User already exists")
        return
    if password != password_confirm:
        print("Passwords does not match")
        return

    user = User(login=login, password=password, email=email)
    user.is_superuser = True
    user.active = True
    user.save()
    print("User was created")
