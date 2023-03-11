
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('panel', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='error',
            field=models.TextField(blank=True, null=True),
        ),
    ]
