# Задание по выбору хранилища
В качестве кандидатов для выбора хранилища для обработки аналитических данных были выбраны ClickHouse и MONGO. Исследование показало, что MONGO быстрее справляется с аналитическими запросами, чем ClickHouse.
Для примера сравним скорость выполнения одинаковых запросов в обеих БД.


### 🚀 Запуск тестов
Чтобы поднять тесты надо выполнить следующие команды 
   (у вас должен быть установлен docker-compose и python3):
- `python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt`
- `docker-compose up -d`
- `python test.py`


### 📙 Описания тестов:
- `select_count` - подсчитать кол-во записей в таблице
  #### запрос: 
      SELECT COUNT(*) FROM view
- `select_count_distinct_movie_id` - подсчитать кол-во записей c уникальными movie_id в таблице
  #### запрос: 
      SELECT count(DISTINCT movie_id) FROM views

- `select_distinct_likes_by_movies_id` - подсчитать кол-во уникальных лайков по каждому фильму
  #### запрос:
      SELECT
         movies_id,
         count(distinct likes)
      FROM views
      GROUP by user_id
- `select_sum_and_max_stars` - найти sum and max stars у каждого фильма 
  #### запрос: 
      SELECT 
            movies_id, 
            sum(stars),
            max(stars) 
        FROM views
        GROUP by movies_id

- `insert_values` - вставка данных в БД
  #### запрос CLICK HOUSE:
      INSERT INTO views VALUES


### 📘 Результаты тестов

| Тест                                 | ClickHouse, sec | MONGO, sec |
|--------------------------------------|:---------------:|:----------:|
| `select_count`                       |     0.0028      |   0.0100   |
| `select_count_distinct_movie_id`     |     0.1183      |   0.2366   |
| `select_distinct_likes_by_movies_id` |   2.6907    |  10.4877   |
| `select_sum_and_max_stars`           |   0.4162    |   1.7255   |
| `insert 10 000 000 rows`             |   179.1    |   182.3    |


Как видно по данным, при схожих параметрах, в запросах на получение и вставку данных Clickhouse обгоняет Vertica в разы.

### Вывод
Было решено использовать MONGO, так как он быстрее справляется с задачами вставки и агрегации.