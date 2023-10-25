from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    """
        Custom User model for the application.
        This model extends the built-in AbstractUser model and adds custom fields for user management.
    """

    username = models.CharField(db_index=True, max_length=255, unique=True, validators=[UnicodeUsernameValidator()])
    telegram_id = models.CharField(db_index=True, max_length=255, unique=True, verbose_name='telegram_login')
    chat_id = models.CharField(verbose_name='telegram_chat_id', blank=True, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        db_table = 'users'


