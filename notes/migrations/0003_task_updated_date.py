# Generated by Django 5.1 on 2024-09-25 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notes', '0002_alter_task_created_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='updated_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
