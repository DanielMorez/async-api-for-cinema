from django.contrib import admin

from notifications.models import Template, Task


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
    list_display = ("title", "type")


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "type",
        "status",
        "template",
        "created_at",
        "updated_at",
        "scheduled_datetime",
        "execution_datetime",
    )
    readonly_fields = ("status",)
    list_filter = ("status", "type")
    search_fields = ("title",)
    raw_id_fields = ("template",)
