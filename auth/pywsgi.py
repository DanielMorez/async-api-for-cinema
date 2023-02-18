from gevent import monkey

monkey.patch_all()

from gevent.pywsgi import WSGIServer
from sentry_sdk.integrations.wsgi import SentryWsgiMiddleware


from app import app

from config import settings


wsgi_app = SentryWsgiMiddleware(app)
http_server = WSGIServer(("", settings.port), wsgi_app)
http_server.serve_forever()
