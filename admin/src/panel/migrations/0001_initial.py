
import django.contrib.postgres.fields.jsonb
import django.db.models.deletion
from django.db import migrations, models

import panel.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Template",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(max_length=250, verbose_name="Наименование"),
                ),
                (
                    "code",
                    models.CharField(
                        choices=[
                            ("welcome_letter", "Приветственное письмо"),
                            ("selection_movies", "Подборка фильмов"),
                            ("personal_newsletter", "Персональная рассылка фильмов"),
                        ],
                        max_length=50,
                    ),
                ),
                ("html", models.TextField()),
                ("subject", models.TextField(blank=True, null=True)),
                ("created_at", models.DateTimeField(editable=False)),
                ("updated_at", models.DateTimeField(editable=False)),
            ],
            options={
                "db_table": "email_templates",
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[(panel.models.NotificationStatuses['to_send'], 'to_send'), (panel.models.NotificationStatuses['in_process'], 'in_process'), (panel.models.NotificationStatuses['done'], 'done'), (panel.models.NotificationStatuses['cancelled'], 'cancelled'), (panel.models.NotificationStatuses['failed'], 'failed')], default=panel.models.NotificationStatuses['to_send'], max_length=250)),
                ('email', models.CharField(max_length=250)),
                ('template_data', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('scheduled_datetime', models.DateTimeField(blank=True, null=True)),
                ('execution_datetime', models.DateTimeField(blank=True, null=True)),
                ('retry_count', models.PositiveIntegerField(default=0)),
                ('hash_sum', models.CharField(max_length=100, unique=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('error_message', models.TextField(blank=True, null=True)),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='panel.template')),
            ],
            options={
                'db_table': 'email_tasks',
            },
        ),
    ]
