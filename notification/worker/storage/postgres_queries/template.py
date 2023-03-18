QUERY = """
    SELECT id, title, subject, content, type 
    FROM notification.templates
    WHERE id = {template_id};
"""