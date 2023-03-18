QUERY = """
    SELECT id, title, subject, content, type, is_personal
    FROM notification.templates
    WHERE id = {template_id};
"""