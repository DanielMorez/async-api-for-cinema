QUERY_TO_GET_LAST_MODIFIED_PERSONS = """
SELECT p.id, p.full_name as name, p.gender, p.modified,
array_agg(DISTINCT pfw.role) as roles,
COALESCE (
       json_agg(
           DISTINCT jsonb_build_object(
               'id', fw.id,
               'title', fw.title,
			   'modified', p.modified
           )
       ) FILTER (WHERE fw.id is not null),
       '[]'
   ) as films
FROM content.person p
LEFT JOIN content.person_film_work pfw ON p.id = pfw.person_id
LEFT JOIN content.film_work fw ON fw.id = pfw.film_work_id
GROUP BY p.id
HAVING GREATEST(p.modified, max(fw.modified))  > '{last_modified}'
ORDER BY p.modified
LIMIT {extract_chunk}
"""