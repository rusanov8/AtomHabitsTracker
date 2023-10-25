from celery import shared_task
from datetime import datetime, date
from django.db.models import Q, F

from habits.models import Habit
from habits.services import telegram_bot


@shared_task
def send_notifications():
    """
    Send notifications for habits to Telegram.

    This Celery task sends notifications for habits that need to be performed today to the respective users' Telegram chats.

    The task fetches habits where the last notification date is yesterday or null (indicating it's the first day of the habit),
     and sends a notification with the habit's details to the user's Telegram chat.

    The last_notification field is then updated to today.
    """

    today = date.today()
    now = datetime.now()

    filtered_habits = Habit.objects.filter(
        Q(last_notification=today - F('days')) |
        Q(last_notification__isnull=True, start_date=today)
    )

    for habit in filtered_habits:
        text = f'Я буду {habit.action} в {habit.location} в {habit.time}'

        telegram_bot(habit.owner.chat_id, text)
        habit.last_notification = today
        habit.save()




