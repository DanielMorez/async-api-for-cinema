
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0002_alter_task_error'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='event_id',
        ),
        migrations.AddField(
            model_name='task',
            name='hash_sum',
            field=models.CharField(max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
