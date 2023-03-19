from django.db import models

from notifications.constants import (
    TEMPLATE_TYPES,
    TASK_STATUS,
    TASK_TYPE,
    CRONTAB_EXAMPLE,
)


class Template(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    content = models.TextField()
    type = models.CharField(max_length=20, choices=TEMPLATE_TYPES)
    is_personal = models.BooleanField(default=False)

    class Meta:
        db_table = "templates"

    def __str__(self):
        return self.title


class Task(models.Model):
    id = models.UUIDField(primary_key=True)
    title = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=TASK_STATUS, default="pending")
    template = models.ForeignKey(Template, on_delete=models.SET_NULL, null=True)
    context = models.JSONField(
        default={},
        help_text="For example, you can fill film ids, user ids or user roles",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # scheduler configs
    type = models.CharField(
        choices=TASK_TYPE, max_length=50, default="send_immediately"
    )
    crontab = models.JSONField(
        help_text=f"Fill crontab like this: {CRONTAB_EXAMPLE}", blank=True, null=True
    )
    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    execution_datetime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = "tasks"
