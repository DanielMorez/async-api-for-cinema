import os
from logging import config as logging_config

from core.logger import LOGGING

# Применяем настройки логирования
logging_config.dictConfig(LOGGING)

# Название проекта. Используется в Swagger-документации
PROJECT_NAME = os.getenv('PROJECT_NAME', 'Тестовый сервис пользовательских данных')
PROJECT_DESCRIPTION = os.getenv('PROJECT_DESCRIPTION',
                                'Тестовый сервис предоставляет информацию о пользователях')
API_VERSION = '1.0.0'

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Адрес API, принимающего события для отправки уведомлений
NOTIFICATION_API_REGISTRATION_EVENT_URL = os.getenv('NOTIFICATION_API_REGISTRATION_EVENT_URL')
