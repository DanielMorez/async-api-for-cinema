from flask import Flask

from db import db, init_db

from models.user import User

app = Flask(__name__)

init_db(app)
app.app_context().push()
db.create_all()


@app.route('/hello-world')
def hello_world():
    return 'Hello, World!'


if __name__ == '__main__':
    app.run()
