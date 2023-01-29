from flask import Flask

from config import Settings
from db import init_db, db, init_migrate
from utils.before_requests.jaeger import configure_tracer, init_jaeger
from utils.routing import register_endpoints
from utils.limiter import init_limiter


def create_app(settings: Settings) -> Flask:
    app = Flask(__name__)
    app.config["DEBUG"] = settings.debug

    app.config["JWT_SECRET_KEY"] = settings.jwt_secrete_key
    app.config["JWT_COOKIE_SECURE"] = settings.jwt_cookie_secure
    app.config["JWT_TOKEN_LOCATION"] = settings.jwt_token_location
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = settings.jwt_access_token_expires
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = settings.jwt_refresh_token_expires

    # routing endpoints
    register_endpoints(app, settings)

    # init database
    init_migrate(app, db)
    init_db(app)
    app.app_context().push()

    if settings.auth_limiter_enable:
        init_limiter(app)

    if settings.request_id_enable:
        configure_tracer(settings.jaeger_host, settings.jaeger_port)
        init_jaeger(app)

    return app
