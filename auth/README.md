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