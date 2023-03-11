import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Template',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250, verbose_name='Наименование')),
                ('code', models.CharField(choices=[('welcome_letter', 'Приветственное письмо')], max_length=50)),
                ('html', models.TextField()),
                ('subject', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
            ],
            options={
                'db_table': 'email_templates',
            },
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_id', models.CharField(max_length=50)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'В процессе исполнения'), (2, 'Выполнена'), (3, 'Отмененен')], default=1)),
                ('email', models.CharField(max_length=250)),
                ('template_data', django.contrib.postgres.fields.jsonb.JSONField(default={})),
                ('scheduled_datetime', models.DateTimeField(blank=True, null=True)),
                ('execution_datetime', models.DateTimeField(blank=True, null=True)),
                ('error', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(editable=False)),
                ('updated_at', models.DateTimeField(editable=False)),
                ('template', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='panel.template')),
            ],
            options={
                'db_table': 'email_tasks',
            },
        ),
    ]
