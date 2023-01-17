# 🔐 Сервис авторизации с системой ролей

## Для разработчиков

- в controllers пишутся endpoints;
- в services пишется логика, которые выполняется endpoint-ами;
- в models пишем модели для работы с таблицами БД. 
  По умолчанию при инициализации БД создается схема `auth`, 
  в которую пишутся все таблицы;

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
(venv) denisduginov@MacBook-Pro-Denis auth % flask create-superuser ADMIN 
User already exists. Try again with another login

```
