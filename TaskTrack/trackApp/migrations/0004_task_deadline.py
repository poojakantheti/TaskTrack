# Generated by Django 3.2.23 on 2024-04-14 20:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trackApp', '0003_auto_20240414_1625'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='deadline',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]