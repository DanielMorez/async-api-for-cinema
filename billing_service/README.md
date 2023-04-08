# Биллинговый сервис

## 🛠 Стек технологий

[![My Skills](https://skillicons.dev/icons?i=python,django,postgres,redis,docker,nginx&perline=6)](https://skillicons.dev)


## 🎡 Схема компонентов

![billing](architecture/billing.png)


## 🪄 Тестирование

0. Поднимите контейнеры `postgres`, `redis`, `auth` и `notification`.
1. Переименуйте `.env.sample` -> `.env`, указав актуальные параметры виртуального окружения.
2. Выполните команды `python manage.py runserver` и `celery -A app worker -B`, чтобы запустить сервис.
