# Логика запроса:
# Фильтрация по <время последнего изменения контента> < максимальное значению modified
# фильма, его участников и жанров

QUERY_TO_GET_LAST_MODIFIED = """
SELECT
   fw.id,
   fw.title,
   fw.description,
   fw.rating,
   fw.type,
   fw.created,
   fw.modified,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name,
			   'modified', p.modified
           )
       ) FILTER (WHERE p.id is not null AND pfw.role = 'actor'),
       '[]'
   ) as actors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role = 'writer'),
       '[]'
   ) as writers,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', p.id,
               'name', p.full_name
           )
       ) FILTER (WHERE p.id is not null AND pfw.role = 'director'),
       '[]'
   ) as directors,
   COALESCE (
       json_agg(
           DISTINCT jsonb_build_object('name', g.name, 'id', g.id)
       ),
       '[]'
   ) as genres
FROM content.film_work fw
LEFT JOIN content.person_film_work pfw ON pfw.film_work_id = fw.id
LEFT JOIN content.person p ON p.id = pfw.person_id
LEFT JOIN content.genre_film_work gfw ON gfw.film_work_id = fw.id
LEFT JOIN content.genre g ON g.id = gfw.genre_id
GROUP BY fw.id
HAVING GREATEST(fw.modified, max(p.modified), max(g.modified))  > '{last_modified}'
ORDER BY fw.modified
LIMIT {extract_chunk};
"""