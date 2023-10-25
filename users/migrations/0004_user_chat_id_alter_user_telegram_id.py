# Generated by Django 4.2.6 on 2023-10-23 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_user_managers'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='chat_id',
            field=models.CharField(blank=True, null=True, verbose_name='telegram_chat_id'),
        ),
        migrations.AlterField(
            model_name='user',
            name='telegram_id',
            field=models.CharField(db_index=True, max_length=255, unique=True, verbose_name='telegram_login'),
        ),
    ]
