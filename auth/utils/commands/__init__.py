from flask import Blueprint

from utils.commands.create_superuser import create_superuser, test_command

cli_bp = Blueprint("app", __name__, cli_group=None)

cli_bp.cli.add_command(create_superuser, "create-superuser")
cli_bp.cli.add_command(test_command, "test")
