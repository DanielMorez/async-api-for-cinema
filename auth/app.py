import logging

from flask_jwt_extended import JWTManager

from config import settings
from utils.app_factory import create_app


logger = logging.getLogger(__name__)


app = create_app(settings)
jwt = JWTManager(app)

if __name__ == "__main__":
    from config import settings
    app.run(host=settings.host, port=settings.port)
