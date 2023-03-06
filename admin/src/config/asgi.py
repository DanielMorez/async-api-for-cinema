import os

from django.core.asgi import get_asgi_application

env_settings = os.getenv('CONFIG_ENV', 'config.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', env_settings)

application = get_asgi_application()
