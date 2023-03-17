QUERY = """
    SELECT id, title, status, context, created_at, updated_at, type, crontab, scheduled_datetime, template_id
    FROM notification.tasks
    WHERE status = 'pending' 
    AND (scheduled_datetime < current_timestamp OR scheduled_datetime IS NULL)
    ORDER BY scheduled_datetime
    LIMIT {extract_chunk};
"""