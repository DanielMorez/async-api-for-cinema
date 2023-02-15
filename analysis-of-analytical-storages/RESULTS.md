# Задание по выбору хранилища
В качестве кандидатов для выбора хранилища для обработки аналитических данных были выбраны ClickHouse, MongoDB и Vertica. Исследоование показало, что ClickHouse быстрее справляется с аналитическими запросами, чем Vertica.
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
- `select_count_distinct_user_id` - подсчитать кол-во записей c уникальными user_id в таблице
  #### запрос: 
      SELECT count(DISTINCT user_id) FROM views
- `select_distinct_movie_by_user` - подсчитать кол-во уникальных просмотренных фильмов по каждому пользователю
  #### запрос:
      SELECT
         user_id,
         count(distinct movie_id)
      FROM views
      GROUP by user_id
- `select_sum_and_max_viewed_frame` - найти sum and max viewed_frame у каждого пользователя
  #### запрос: 
      SELECT 
            user_id, 
            sum(viewed_frame),
            max(viewed_frame) 
        FROM views
        GROUP by user_id
- `select_sum_and_max_viewed_frame_with_where` - найти sum and max viewed_frame у каждого пользователя с условием event_time > '2021-04-13 23:09:02'
  #### запрос:
      SELECT 
            user_id, 
            sum(viewed_frame),
            max(viewed_frame) 
        FROM views
        WHERE event_time > '2021-04-13 23:09:02'
        GROUP by user_id
- `insert_values` - вставка данных в БД
  #### запрос CLICK HOUSE:
      INSERT INTO views VALUES
  #### запрос VERTICA:
      INSERT INTO views (
         id, 
         user_id,
         movie_id,
         viewed_frame,
         event_time
      )
      VALUES (%s,%s,%s,%s,%s)'

### 📘 Результаты тестов

| Тест | ClickHouse, sec | Vertica, sec |
|---|:---------------:|:------------:|
| `select_count` |     0.0028      |    0.0100   |
| `select_count_distinct_movie_id` |     0.1183      |    0.2366    |
| `select_count_distinct_user_id` |     0.1219      |  0.6363  |
| `select_distinct_movie_by_user` |   2.6907    |  10.4877  |
| `select_sum_and_max_viewed_frame` |   0.4162    |  1.7255  |
| `select_sum_and_max_viewed_frame_with_where` |   0.3859    |  1.9968  |
| `insert 10 000 000 rows` |   179.1    |  182.3  |


Как видно по данным, при схожих параметрах, в запросах на получение и вставку данных Clickhouse обгоняет Vertica в разы.

### Вывод
Было решено использовать  , так как он быстрее справляется с задачами вставки и агрегации.