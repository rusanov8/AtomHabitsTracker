from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitValidation(APITestCase):
    """
        Test cases for validating habit creation and related conditions.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username='test_user',
            password='testpassword',
            telegram_id='@test_user_tg'
        )

        self.client.force_authenticate(user=self.user)

        self.habit_data = {
            "owner": self.user,
            "action": "test_habit",
            "location": "test_location",
            "time": "00:00",
            "periodicity": "daily",
            "execution_time": "60",
            "start_date": "2023-10-24",
            "is_public": True,
            "is_pleasant": True,
        }

    def test_create_pleasant_habit_with_reward(self):
        """
            Test creating a pleasant habit with a reward, which is not allowed.
        """

        data = self.habit_data
        data['reward'] = 'test_reward'

        response = self.client.post(
            '/habits/create', data
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Habit.objects.all().exists())
        self.assertEqual(response_data['non_field_errors'][0],
                         'Error: A pleasant habit cannot have a reward or a related habit.')


    def test_related_habit_is_only_pleasant(self):

        test_related_habit_unpleasant = Habit.objects.create(
            owner=self.user,
            action="unpleasant_related_test_habit",
            location="test_location",
            time="00:00",
            periodicity="daily",
            execution_time="100",
            start_date="2023-10-24",
            is_public=True,
            is_pleasant=False,

        )

        initial_habits_count = Habit.objects.count()

        data = self.habit_data
        data['related_habit'] = test_related_habit_unpleasant.id

        response = self.client.post(
            '/habits/create', data
        )
        final_habit_count = Habit.objects.count()
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(initial_habits_count, final_habit_count)
        self.assertEqual(response_data['related_habit'][0],
                         'Error: Only pleasant habits can be related to this habit.')


    def test_create_pleasant_habit_with_related_habit(self):
        """
            Test creating a habit with a related habit that is not pleasant.
            """
        test_related_habit_pleasant = Habit.objects.create(
            owner=self.user,
            action="pleasant_related_test_habit",
            location="test_location",
            time="00:00",
            periodicity="daily",
            execution_time="100",
            start_date="2023-10-24",
            is_public=True,
            is_pleasant=True,

        )

        data = self.habit_data
        data['related_habit'] = test_related_habit_pleasant.id

        response = self.client.post(
            '/habits/create', data
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response_data['non_field_errors'][0],
                         'Error: A pleasant habit cannot have a reward or a related habit.')
        self.assertEqual(Habit.objects.count(), 1)




