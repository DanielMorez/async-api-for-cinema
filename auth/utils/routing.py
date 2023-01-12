def register_endpoints(app):
    from resources import auth_bp

    app.register_blueprint(auth_bp)
