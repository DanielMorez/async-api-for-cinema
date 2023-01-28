from config import Settings
from utils.before_requests import before_requests_bp


def register_endpoints(app, settings: Settings):
    from resources import auth_bp
    from utils.commands import cli_bp

    app.register_blueprint(auth_bp)  # API
    app.register_blueprint(cli_bp)  # CLI

    if settings.request_id_enable:
        app.register_blueprint(before_requests_bp)
