Ссылка на проект https://github.com/DanielMorez/async-api-for-cinema 
Участники @DanielMorez, @RuslanYankov, @LenchikTs

# 🔐 Сервис авторизации с системой ролей

## Основные сущности
- Пользователи - логин, пароль, является ли суперюзером, email.
- Роль - имя.
- Пользователь-Роль - пользователь, роль.
- История аутентификации - клиент входа (агент), устройство, дата и время посещения.

## 🏃‍♂️Список endpoints
Для тестирования через [OpenAPI] необходимо перейти по адресу:
http://localhost/

## Представленные enpoints:

* `Управление ролями`:
- Создание роли: POST /api/v1/auth/roles
- Получение списка существующих ролей: GET /api/v1/auth/roles
- Изменение роли по ее идентификатору в теле зарпоса: PUT /api/v1/auth/roles
- Удаление роли: DELETE /api/v1/user/auth/roles

* `Управление авторизацией`:
- Создание пользователя: POST /api/v1/auth/user/register
- Авторизация пользователя: POST /api/v1/auth/user/login
- Выход пользователя (помещает переданные токены в блэклист): POST /api/v1/auth/user/logout
- Для валидного refresh-токена возвращает пару токенов access+refresh: POST /api/v1/auth/token-refresh
- История аутентификации: GET /api/v1/auth/user/login-histories

* `Управление профилем пользователя`:
- Получение данных пользователя: GET /api/v1/auth/user/profile
- Заполнение карточки пользователя (first_name, last_name, email): PATCH /api/v1/auth/user/profile
- Изменение пароля пользователя: POST /api/v1/auth/user/change-password
- Изменение логина пользователя: POST /api/v1/auth/user/change-login

* `Управление пользователем`:
- Назначить пользователю роль: POST /api/v1/auth/user-role
- Получение списка ролей пользователя: GET /api/v1/auth/user-role
- Отобрать у пользователя роль: DELETE /api/v1/auth/user-role

## 🏃‍♂️ Запуск функии создания superuser-a

B терминале вводим при запущенных контейнерах и `app.py` строку типа:
`flask app create-superuser <login_supersuser-a>`
Затем следуем инструкциям и вводим: <password>, <password_confirmation> и <email> (необязательный параметр);
