
from django.db import migrations, models
import panel.models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0003_auto_20230311_1351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.CharField(choices=[(panel.models.Task.NotificationStatuses['to_send'], 'to_send'), (panel.models.Task.NotificationStatuses['in_process'], 'in_process'), (panel.models.Task.NotificationStatuses['done'], 'done'), (panel.models.Task.NotificationStatuses['cancelled'], 'cancelled'), (panel.models.Task.NotificationStatuses['failed'], 'failed')], default=panel.models.Task.NotificationStatuses['to_send'], max_length=250),
        ),
        migrations.AlterField(
            model_name='template',
            name='code',
            field=models.CharField(choices=[('welcome_letter', 'Приветственное письмо'), ('selection_movies', 'Подборка фильмов'), ('personal_newsletter', 'Персональная рассылка фильмов')], max_length=50),
        ),
    ]
