# 📧 Сервис нотификации

## 🛠 Стек технологий

[![My Skills](https://skillicons.dev/icons?i=python,fastapi,rabbitmq,docker,nginx&perline=5)](https://skillicons.dev)


## 🔑 Окружение

Добавьте в `.env` `SMTP__EMAIL` и `SMTP__PASSWORD` для корректной работы сервиса


## 📚 Административная панель

Здесь можно создать таску для рассылки писем указав фильтр для сегментации пользователей. Для упрощения задачи сделали два фильтра.

```python
{
    "user_filters": {
        "has_enail": True
    }  # Получить пользователей с email
}
```

```python
{
    "user_ids": [
        "b08486ad-5e93-485b-ba7a-7efc1319ebdf"
    ]  # Отправить только этим пользователям
}
```

Так же здесь можно отложить выполнение рассылки до заданного времени, заполнив поле
`scheduled_datetime`


## 📬 Шедулер

С определенным интервалом проверяет записи в таблице таск по условию

```postgresql
SELECT id, title, status, context, created_at, updated_at, type, crontab, scheduled_datetime, template_id
FROM notification.tasks
WHERE status = 'pending' 
AND (scheduled_datetime < current_timestamp OR scheduled_datetime IS NULL)
ORDER BY scheduled_datetime
LIMIT {extract_chunk};
```

В зависимости от фильтров указанных в `context` формирует список `user_ids` (если он оказывается пустым, то отменяет таску - `canceled`)
После успешной отправки выставляет статус `done`.

```postgresql
UPDATE notification.tasks SET status = '{status}' WHERE id = '{task_id}';
```

## 🚀 API

Имеет два метода для отправки уведомления, протестировать их можно здесь `http://localhost/api/notifications/openapi#`

1. Метод для отправки любого сообщения с выбранным тимплейтом и контентом
2. Метод для отправки приветственного пиьсма (реализация первого метода, но с зашитым тимплейтом)

Пример запроса

```commandline
curl -X 'POST' \
  'http://localhost:8002/notifications/send' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "type": "send_immediately",
  "template_id": 1,
  "user_ids": [
    "b08486ad-5e93-485b-ba7a-7efc1319ebdf"
  ],
  "context": {"user_filters": {"has_email": true}}
}'
```

Методы перекладывают полученные уведомления в очередь RabbitMQ


## 🎢 Воркер

Прослушивает очередь RabbitMQ, и если появляется уведомление, то персонализирует данные по `user_ids` и забирает шаблон пиьсма по `template_id`
и отправляет сообщение по указанному в аккаунте email-у