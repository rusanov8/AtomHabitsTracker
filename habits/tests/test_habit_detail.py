from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitDetail(APITestCase):
    """
        Test cases for retrieving habit details using the HabitDetail API endpoint.
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


    def test_habit_detail_if_owner(self):
        """
            Test retrieving habit details by the owner.
        """

        habit = Habit.objects.create(**self.habit_data)

        self.client.force_authenticate(user=self.owner_user)

        response = self.client.get(f'/habits/{habit.id}')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data,
                         {'action': 'test_public_habit', 'location': 'test_location', 'time': '00:00:00',
                          'is_pleasant': True, 'periodicity': 'daily', 'reward': None, 'execution_time': 60,
                          'is_public': True, 'start_date': '2023-10-24', 'related_habit': None})



    def test_habit_detail_if_not_owner(self):
        """
            Test retrieving habit details by a user who is not the owner.
        """

        habit = Habit.objects.create(**self.habit_data)

        self.client.force_authenticate(user=self.user)

        response = self.client.get(f'/habits/{habit.id}')
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data,
                         {'action': 'test_public_habit', 'location': 'test_location', 'time': '00:00:00',
                          'is_pleasant': True, 'periodicity': 'daily', 'execution_time': 60, 'is_public': True})



    def test_habit_detail_if_not_authorized(self):
        """
            Test retrieving habit details when not authorized (unauthenticated).
        """
        habit = Habit.objects.create(**self.habit_data)

        response = self.client.get(f'/habits/{habit.id}')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)





