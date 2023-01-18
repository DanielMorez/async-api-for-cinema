# 🔐 Сервис авторизации с системой ролей

## Для разработчиков

- В `controllers` пишутся endpoints;
- В `services` пишется логика, которые выполняется endpoint-ами;
- В `models` пишем модели для работы с таблицами БД. 
  По умолчанию при инициализации БД создается схема `auth`, 
  в которую пишутся все таблицы;
- В `utils/namespace` и `utils/parser` создаются пространства, ответы и ожидаемые данные для описания эндпоинтов;
- В `utils/commands` разрабатываются кастомные команды (например, create-superuser);
- В `utils/routing` происходит регистрация приложений;

## 🔑 Окружение

1. Уберите префиксы у `.env.local` или `.env.dist`, 
   чтобы получилось `.env`.

### Какой `.env` выбрать❔

1. Для локальной разработки `.env.local`.

2. Для запуска тестов в docker-compose используйте `.env.dist`.

## 🏃‍♂️ Запуск приложения

- в режиме дебаг `python app.py` (выставите debug = True в .env);
- в режиме продакшн `python pywsgi.py` (выставите debug = False в .env);

## 🦸‍♂️ Создать суперпользователя

Для этого необходимо перейти в `auth` и ввести команду.
```commandline
flask create-superuser <login>
```
После чего вам предложат ввести пароль, подтвердить его и email. Итоговый вывод в консоли может выглядеть вот так:
```commandline
(venv) developer@MacBook-Pro auth % flask --app app create-superuser ADMIN
Enter password: ADMIN
Confirm password: ADMIN
Enter email (optional): 
Superuser was successfully created
(venv) developer@MacBook-Pro auth % flask create-superuser ADMIN 
User already exists. Try again with another login

```

## 📚 OpenAPI

Для просмотра документации перейдите по `http://0.0.0.0:5000/api/v1/user/` 
