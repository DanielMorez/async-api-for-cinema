import click
import logging

from models import User


logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@click.command()
@click.argument("login")
def create_superuser(login: str):
    if User.find_by_login(login):
        logger.error("User already exists.")
        return
    password = input("Enter password: ")
    password_confirmation = input("Confirm password: ")
    if password != password_confirmation:
        logger.error("Passwords do not match.")
        return

    email = input("Enter email (optional): ")
    try:
        user = User(login=login, password=password, email=email)
        user.is_superuser = True
        user.active = True
        user.save()
        logger.debug("Superuser was created.")
        return
    except Exception as error:
        logger.error(f"Error: {error}")
        return
