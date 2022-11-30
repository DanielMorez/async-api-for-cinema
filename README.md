# async-api-for-cinema
Реализация асинхронного API для кинотеатра

## 🚀 Быстрый старт для разработчика

1. Чтобы развернуть проект в среде разработки, воспользуйтесь одной из команд: 
- `make dev docker`
- `docker compose -f docker-compose.dev.yml up --build`

2. Перейдите в директорию `async-api/src/` и переименуйте `.env.local` в `.env`, чтобы было удобно локально вести разработку

3. Создайте виртуальное окружение в `async-api`: `python3.10 -m venv venv`

4. Активируйте виртуальное окружение `source venv/bin/activate`

5. Вернитесь в корень проекта и накатите миграции: `make init migrations`

6. Чтобы запустить `async-api` перейдите в директорию `async-api/src/` и выполните команду: `python main.py`

В итоге, у вас дожно появится такое сообщение:

```commandline
async_api                | 2022-11-28 20:40:48,652 - uvicorn.error - INFO - Started server process [1]
async_api                | 2022-11-28 20:40:48,652 - uvicorn.error - INFO - Waiting for application startup.
async_api                | 2022-11-28 20:40:48,653 - uvicorn.error - INFO - Application startup complete.
async_api                | 2022-11-28 20:40:48,655 - uvicorn.error - INFO - Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

```


P.S. Не забудьте накатить миграции, для этого в корне проекта выполните команду: `make init migrations`
