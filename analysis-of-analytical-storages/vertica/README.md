*Выполнение запросов во время записи данных*

Executing query

    SELECT COUNT(*) FROM views

[420000]

Query execution took: 
0.02783513069152832


Executing query
    
    SELECT count(DISTINCT movie_id) FROM views

[10000]
Query execution took: 
0.2515218257904053


Executing query

    SELECT count(DISTINCT user_id) FROM views

[10000]
Query execution took: 
0.22393584251403809


Executing query

    SELECT 
        user_id, 
        count(distinct movie_id) 
    FROM views
    GROUP by user_id
    
Query execution took: 
2.4797160625457764


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    GROUP by user_id
    
Query execution took: 
0.4341411590576172


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    WHERE event_time > '2021-04-13 23:09:02'
    GROUP by user_id
    
Query execution took: 
0.4405517578125


Executing insert query. Rows: 10

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

0.24517130851745605


Executing insert query. Rows: 100

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

1.9224703311920166


Executing insert query. Rows: 1000

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

19.16924285888672


Executing query

    SELECT COUNT(*) FROM views

[426110]
Query execution took: 
0.020767927169799805


*Выполнение запросов при 3 млн записей*
Executing query

    SELECT COUNT(*) FROM views

[2570440]
Query execution took: 
0.04602789878845215


Executing query

    SELECT count(DISTINCT movie_id) FROM views

[10000]
Query execution took: 
1.0024330615997314


Executing query

    SELECT count(DISTINCT user_id) FROM views

[10000]
Query execution took: 
1.509639024734497


Executing query

    SELECT
        user_id,
        count(movie_id)
    FROM views
    GROUP by user_id
    
Query execution took: 
2.2240471839904785


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    GROUP by user_id
    
Query execution took: 
3.720479965209961


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    WHERE event_time > '2021-04-13 23:09:02'
    GROUP by user_id
    
Query execution took: 
4.0213212966918945


Executing insert query. Rows: 10

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

0.2113478183746338


Executing insert query. Rows: 100

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

1.933547019958496


Executing insert query. Rows: 1000

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

20.56726098060608


Executing query

    SELECT COUNT(*) FROM views

[2579550]

Query execution took:
0.03425097465515137

*Выполнение запросов при 7 млн записей*
Executing query

    SELECT COUNT(*) FROM views

[7931550]
Query execution took: 
0.23443937301635742


Executing query

    SELECT count(DISTINCT movie_id) FROM views

[10000]
Query execution took: 
6.370495080947876


Executing query
    
    SELECT count(DISTINCT user_id) FROM views

[10000]
Query execution took: 
7.4493937492370605


Executing query

    SELECT
        user_id,
        count(movie_id)
    FROM views
    GROUP by user_id
    
Query execution took: 
9.397538661956787


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    GROUP by user_id
    
Query execution took: 
14.479244947433472


Executing query

    SELECT 
        user_id, 
        sum(viewed_frame),
        max(viewed_frame) 
    FROM views
    WHERE event_time > '2021-04-13 23:09:02'
    GROUP by user_id
    
Query execution took: 
13.69877004623413


Executing insert query. Rows: 10

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

0.22550606727600098


Executing insert query. Rows: 100

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

2.3532750606536865


Executing insert query. Rows: 1000

    INSERT INTO views (user_id, movie_id, viewed_frame, event_time) VALUES (?,?,?,?)

22.386600971221924


Executing query

    SELECT COUNT(*) FROM views

[7948660]
Query execution took: 
0.08531904220581055