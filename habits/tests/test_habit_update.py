from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitUpdate(APITestCase):
    """
        Test cases for updating habits using the HabitUpdate API endpoint.
    """

    def setUp(self):
        """
            Set up data for each test case.
        """

        self.owner_user = User.objects.create_user(
            username='owner_user',
            password='testpassword',
            telegram_id='@owner_user'
        )

        self.user = User.objects.create_user(
            username='test_user',
            password='testpassword',
            telegram_id='@test_user_tg'
        )

        self.habit_data = {
            "owner": self.owner_user,
            "action": "test_public_habit",
            "location": "test_location",
            "time": "00:00",
            "periodicity": "daily",
            "execution_time": "60",
            "start_date": "2023-10-24",
            "is_public": True,
            "is_pleasant": True,
        }


    def test_update_habit_if_owner(self):
        """
            Test updating a habit by the owner.
        """

        habit = Habit.objects.create(**self.habit_data)

        updated_data = {
            "action": "updated_habit_action",
        }

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.put(f'/habits/edit/{habit.id}',
                                   updated_data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Habit.objects.all().first().action, updated_data['action'])


    def test_update_habit_if_not_owner(self):
        """
            Test updating a habit by a user who is not the owner.
        """

        habit = Habit.objects.create(**self.habit_data)

        updated_data = {
            "execution_time": 12,
        }

        self.client.force_authenticate(user=self.user)

        response = self.client.put(f'/habits/edit/{habit.id}',
                                   updated_data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
