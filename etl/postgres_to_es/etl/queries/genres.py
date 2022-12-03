QUERY_TO_GET_LAST_MODIFIED_GENRES = """
SELECT g.id, g.name, g.description, g.modified
FROM content.genre g
GROUP BY g.id
HAVING GREATEST(g.modified, max(g.modified))  > '{last_modified}'
ORDER BY g.modified
LIMIT {extract_chunk}
"""