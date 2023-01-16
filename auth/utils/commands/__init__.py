from flask import Blueprint

from utils.commands.create_superuser import create_superuser

cli_bp = Blueprint("app", __name__)

cli_bp.cli.add_command(create_superuser, "create-superuser")
