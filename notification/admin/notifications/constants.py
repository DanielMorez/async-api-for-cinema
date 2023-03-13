TEMPLATE_TYPES = (("email", "email"),)

TASK_STATUS = (
    ("pending", "В очереди на отправку"),
    ("done", "Отправлено"),
    ("canceled", "Отмненено"),
)

TASK_TYPE = (
    ("send_immediately", "Отправить сразу"),
    ("regular_mailing", "Регулярная рассылка"),
)

CRONTAB_EXAMPLE = (
    "https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html#crontab-schedules"
)
