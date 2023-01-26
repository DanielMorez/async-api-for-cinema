from flask_limiter import Limiter, ExemptionScope
from flask_limiter.util import get_remote_address


def register_endpoints(app):
    from resources import auth_bp
    from utils.commands import cli_bp

    limiter = Limiter(get_remote_address,
                      app=app,
                      default_limits=["200 per day", "50 per hour"]
                      )

    app.register_blueprint(auth_bp)  # API
    app.register_blueprint(cli_bp)  # CLI

#можете раскомментить и потестить, рабочая версия - default_limits
    # limiter.limit("2/minute")(auth_bp)
    # limiter.limit("3/minute")(cli_bp)

    limiter.exempt(
        flags=ExemptionScope.DEFAULT|ExemptionScope.APPLICATION|ExemptionScope.ANCESTORS
    )
