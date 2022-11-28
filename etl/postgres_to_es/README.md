# Краткое описание запуска проекта

## Быстрый cтарт (docker-compose)

- переходим в директорию etl;
- поднимаем Postgres, Redis, ElasticSearch, а также сервис по переносу данных: 
`docker compose -f docker-compose.dev.yml --env-file postgres_to_es/.env up --build`
- перегоняем данные из Sqlite в Postgres (чтобы было что грузить в Elasticsearch):
`make postgres-content-local`
- создаем индекс movie в Elasticsearch: 
`make movies-index`

## Развертывание через Dockerfile

Убедитесь, что у вас правильно настроено виртуальное окружение в .env

А затем выполните следующие команды:

- `docker build postgres_to_es .`
- `docker run --rm -d --network=host postgres_to_es`