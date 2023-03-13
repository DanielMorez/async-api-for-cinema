# Задание по выбору хранилища
В качестве кандидатов для выбора хранилища для обработки  данных были выбраны  Postgres и MONGO. Исследование показало, что MONGO быстрее справляется с аналитическими запросами, чем ClickHouse.
Для примера сравним скорость выполнения одинаковых запросов в обеих БД.


### 🚀 Запуск тестов
Чтобы поднять тесты надо выполнить следующие команды 
   (у вас должен быть установлен docker-compose и python3):
- `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- `docker-compose up -d`
- `python tests/test_bookmarks.py`

### 📙 Описания тестов:

  #### запрос: 
- `INSERT INTO public.{table}{columns} VALUES` \ collection.insert_one(params) - вставить  запись в таблице

  #### запрос:
- `DELETE FROM public.{table} WHERE` \ collection.delete_one(params) - удалить запись в таблице

  #### запрос: 
- `SELECT * FROM public.{table} WHERE` \ collection.find(params) - найти запись в таблице


### 📘 Результаты тестов - выполняются при указанном в столбце количестве записей в БД

| Тест             | Insert, microsec | Find, microsec | Delete , microsec |
|------------------|:-----------:|:---------:|:---------:| 
| Postgres 50 000  |   1.140    |  0.583  | 0.613 |
| Postgres 100 000 |   1.785    |   0.691  | 0.713 |
| Postgres 500 000 |    2.457    |   0.723   | 0.802 |
| Postgres 1 000 000 |    2.531    |   0.983   | 1.013 |
| MONGO 50 000     |   0.609    |  0.575  | 0.623 |
| MONGO 100 000    |   1.002    |   0.659  | 0.702 |
| MONGO 500 000    |    1.41    |   0.720   | 0.783 |
| MONGO 1 000 000  |    1.821    |   0.973   | 0.988 |

Как видно по данным, при схожих параметрах, в запросах на получение данных MONGO обгоняет Postgres в разы.

### Вывод
Было решено использовать MONGO, так как он быстрее справляется с задачами вставки и агрегации.