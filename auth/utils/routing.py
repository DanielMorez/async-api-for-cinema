def register_endpoints(app):
    from resources import auth_bp
    from utils.commands import cli_bp

    app.register_blueprint(auth_bp)  # API
    app.register_blueprint(cli_bp)  # CLI
