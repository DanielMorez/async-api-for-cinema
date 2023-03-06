# Generated by Django 4.0.1 on 2022-02-01 14:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_panel', '0003_alter_template_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='template',
            name='code',
            field=models.CharField(choices=[('common', 'Обычное письмо'), ('monthly_personal_statistic', 'Ежемесячная персональная статистика')], max_length=50),
        ),
    ]
