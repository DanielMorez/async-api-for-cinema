from flask_jwt_extended import JWTManager

from config import settings
from utils.app_factory import create_app

app = create_app(settings)
jwt = JWTManager(app)


if __name__ == "__main__":
    app.run()
