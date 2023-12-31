# Generated by Django 4.2.6 on 2023-10-19 05:09

import django.contrib.auth.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='user',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='Telegram'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(db_index=True, max_length=255, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()]),
        ),
    ]
