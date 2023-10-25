from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitDelete(APITestCase):
    """
        Test cases for deleting habits using the HabitDelete API endpoint.
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


    def test_delete_habit_if_owner(self):
        """
            Test deleting a habit by the owner.
        """

        habit = Habit.objects.create(**self.habit_data)
        initial_habit_count = Habit.objects.count()

        self.client.force_authenticate(user=self.owner_user)
        response = self.client.delete(f'/habits/delete/{habit.id}')

        final_habit_count = Habit.objects.count()

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(final_habit_count, initial_habit_count - 1)



    def test_delete_habit_if_not_owner(self):
        """
            Test deleting a habit by a user who is not the owner (forbidden).
        """

        habit = Habit.objects.create(**self.habit_data)
        initial_habit_count = Habit.objects.count()

        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f'/habits/delete/{habit.id}')

        final_habit_count = Habit.objects.count()

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(final_habit_count, initial_habit_count)


