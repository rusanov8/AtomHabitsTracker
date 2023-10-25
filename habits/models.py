from django.core.validators import MaxValueValidator
from django.db import models
from rest_framework.serializers import ValidationError

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Habit(models.Model):
    """ Represents a habit created by a user. """

    owner = models.ForeignKey(User, db_index=True, on_delete=models.CASCADE, verbose_name='Owner', related_name='habits')
    action = models.CharField(max_length=255, verbose_name='Action')
    location = models.CharField(max_length=100, verbose_name='Location')
    time = models.TimeField(verbose_name='Time of execution')

    is_pleasant = models.BooleanField(default=False, verbose_name='Pleasant habit')
    related_habit = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='Related habit', **NULLABLE)
    periodicity = models.CharField(max_length=50, verbose_name='Periodicity')
    days = models.PositiveIntegerField(verbose_name='Days of period')
    reward = models.CharField(max_length=255, verbose_name='Reward', **NULLABLE)
    execution_time = models.PositiveIntegerField(validators=[MaxValueValidator(120)],
                                                 verbose_name='Execution time')
    is_public = models.BooleanField(default=False, verbose_name='Public habit')
    start_date = models.DateField(verbose_name='Start date')
    last_notification = models.DateField(null=True, blank=True, verbose_name='Last notification date')

    def __str__(self):
        return self.action

    def save(self, *args, **kwargs):
        """Save the habit with adjusted 'days' value based on 'periodicity'. """

        if self.periodicity == 'daily':
            self.days = 1
        elif self.periodicity == 'every_other_day':
            self.days = 2
        elif self.periodicity == 'every_third_day':
            self.days = 3
        elif self.periodicity == 'every_fourth_day':
            self.days = 4
        elif self.periodicity == 'every_fifth_day':
            self.days = 5
        elif self.periodicity == 'every_sixth_day':
            self.days = 6
        elif self.periodicity == 'weekly':
            self.days = 7
        super().save(*args, **kwargs)

    def clean(self):
        """Checks if the habit references itself, which is not allowed. """

        if self.related_habit == self:
            raise ValidationError("A habit cannot reference itself.")
        super(Habit, self).clean()

    class Meta:
        verbose_name = 'habit'
        verbose_name_plural = 'habits'
        db_table = 'habits'
