import click

from models import User


@click.command()
@click.argument("login")
def create_superuser(login: str):
    if User.find_by_login(login):
        print("User already exists. Try again with another login")
        return
    password = input("Enter password: ")
    password_confirmation = input("Confirm password: ")
    if password != password_confirmation:
        print("Passwords do not match. Superuser wasn't created")
        return

    email = input("Enter email (optional): ")
    try:
        user = User(login=login, password=password, email=email)
        user.is_superuser = True
        user.active = True
        user.save()
        print("Superuser was successfully created")
        return
    except Exception as error:
        print(error)
        return
