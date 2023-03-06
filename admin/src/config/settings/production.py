import os

from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('PG_DBNAME', 'notifications'),
        'USER': os.getenv('PG_USER', 'postgres'),
        'PASSWORD': os.getenv('PG_PASSWD', 'postgres'),
        'HOST': os.getenv('PG_HOST', 'postgres'),
        'PORT': os.getenv('PG_PORT', '5432'),
    }
}
