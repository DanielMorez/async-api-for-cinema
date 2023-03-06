import os

from django.core.wsgi import get_wsgi_application

env_settings = os.getenv('CONFIG_ENV', 'config.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_settings)

application = get_wsgi_application()
