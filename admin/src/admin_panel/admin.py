from django.contrib import admin

from .models import MailingTask, Template


@admin.register(Template)
class TemplatesAdmin(admin.ModelAdmin):
    """Admin interface for Template."""


@admin.register(MailingTask)
class TasksAdmin(admin.ModelAdmin):
    """Admin interface for Task."""
