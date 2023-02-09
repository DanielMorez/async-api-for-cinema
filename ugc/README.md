# 📦 BigData | Сервис генерации пользовательского контента

## 🛠 Стек технологий

[![My Skills](https://skillicons.dev/icons?i=python,fastapi,kafka,docker,nginx&perline=5)](https://skillicons.dev)


## 🧭 Для разработчиков

- В `adapters` разаработан брокер сообщений.
- В  `api/v1` разаработываются приложения сервиса. Например, приложение `view_films` ответчает за просмотры фильмов пользователем.
- В `auth` разаработана middleware и модель пользователя, которая на каждый запрос вешает проверку авторизации.
- В `core` лежат настройки сервиса.
- В `openapi` лежат константы для документации. Так, после добавления приложения туда можно прикрепить его описание по тегу.
- В `services` лежит логика работы эндпоинтов.


## 🔑 Окружение

- `.env.dev` используется для локальной разработки.
- `.env` для запуска всего проекта.


## 🏃‍♂️ Запуск приложения в режиме разработчика / дебага

- С помощью команды `make ugc depends on` запустите cервисы аутентификации и kafka.
- Выполните команду `python main.py`.

В итоге, у вас в терминале должен быть примерно следующий вывод.

```commandline
2023-02-10 03:36:50,395 - uvicorn.error - INFO - Started server process [41289]
2023-02-10 03:36:50,395 - uvicorn.error - INFO - Waiting for application startup.
2023-02-10 03:36:50,448 - uvicorn.error - INFO - Application startup complete.
2023-02-10 03:36:50,449 - uvicorn.error - INFO - Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
```

- Получите access токен по этой ссылке `http://localhost:5001/api/v1/user/`.
- Перейдите в `http://localhost:8001/api/ugc/openapi`.
- Вставьте access токен в заголовок и сделайте запрос.


## 📨 Kafka

После того как вы сделаете запрос, сообщение запишется в брокер.
Посмотреть это сообщение можно здесь `http://localhost:9999/topic/views/messages`


## ♻️ ETL

`pass`

## 📊 ClickHouse

`pass`