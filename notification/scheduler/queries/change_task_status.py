QUERY = """
    UPDATE notification.tasks SET status = '{status}' WHERE id = '{task_id}';
"""