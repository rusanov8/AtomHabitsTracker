from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitList(APITestCase):
    """
        Test cases for listing habits using the HabitList API endpoint.
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

    def test_habits_list_if_not_authorised(self):
        """
            Test listing public habits when not authorized (unauthenticated).
        """
        public_habit_data = self.habit_data

        Habit.objects.create(**public_habit_data)

        response = self.client.get('/habits/public')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_public_habits_list(self):
        """
            Test listing public habits when authorized as a user.
        """

        public_habit_data = self.habit_data

        private_habit_data = public_habit_data
        private_habit_data['is_public'] = False
        private_habit_data['action'] = 'test_private_habit'

        Habit.objects.create(public_habit_data)

        Habit.objects.create(private_habit_data)

        self.client.force_authenticate(user=self.user)
        response = self.client.get('/habits/public')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.json()), 1)
        self.assertEqual(response.json(), [{'action': 'test_public_habit', 'periodicity': 'daily'}])


    def test_own_habits_list(self):
        """
            Test listing habits owned by the authenticated user.
        """

        Habit.objects.create(**self.habit_data)

        self.client.force_authenticate(user=self.owner_user)
        response = self.client.get('/habits')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_data = response.json()
        self.assertEqual(response_data['results'], [{'action': 'test_public_habit', 'periodicity': 'daily'}])








