from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from app import app

from config import settings


http_server = WSGIServer(("", settings.port), app)
http_server.serve_forever()
