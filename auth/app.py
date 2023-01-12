from flask import Flask

from createsuperuser import bp
from config import settings
from db import db, init_db

from models.user import User
from models.login_history import LoginHistory

app = Flask(__name__)
app.register_blueprint(bp, url_prefix='/superuser')
init_db(app)
app.app_context().push()
db.create_all()

user = User(login="test", password="test", email="test@mail.com")
user.save()

login_history = LoginHistory(
    user_id=user.id, user_agent="Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1"
)
login_history.save()


@app.route("/hello-world")
def hello_world():
    return "Hello, World!"


if __name__ == "__main__":
    app.run(
        host=settings.host,
        port=settings.port,
        debug=settings.debug
    )
