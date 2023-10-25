from rest_framework import status
from rest_framework.test import APITestCase

from habits.models import Habit
from users.models import User


class TestHabitCreation(APITestCase):
    """
        Test cases for creating habits using the HabitCreate API endpoint.
    """

    def setUp(self):
        """
        Set up data for each test case.
        """
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


    def test_create_habit(self):
        """
            Test creating a habit using the 'create' endpoint.
        """

        data = self.habit_data

        response = self.client.post(
            '/habits/create', data
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Habit.objects.all().exists())
        self.assertEqual(response_data['action'], data['action'])


    def test_create_habit_with_reward_and_related_habit(self):
        """
            Test creating a habit with both a reward and a related habit, which is not allowed.
         """

        test_reward_habit = Habit.objects.create(
            owner=self.user,
            action="reward_test_habit",
            location="test_location",
            time="00:00",
            periodicity="daily",
            execution_time="100",
            start_date="2023-10-24",
            is_public=True,
            is_pleasant=True,

        )

        initial_habits_count = Habit.objects.count()

        data = self.habit_data
        data['reward'] = 'test_reward'
        data['related_habit'] = test_reward_habit.id


        response = self.client.post(
            '/habits/create', data
        )

        final_habit_count = Habit.objects.count()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(final_habit_count, initial_habits_count)

        response_data = response.json()
        self.assertEqual(response_data['non_field_errors'][0],
                         'Error: Choose either a related habit or specify a reward, but not both simultaneously.')


    def test_habit_execution_time(self):
        """
            Test creating a habit with an execution time exceeding the allowed limit.
         """

        data = self.habit_data
        data['execution_time'] = 121

        response = self.client.post(
            '/habits/create', data
        )

        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Habit.objects.all().exists())
        self.assertEqual(response_data['execution_time'][0], 'Ensure this value is less than or equal to 120.')

        self.assertFalse(Habit.objects.all().exists())


    def test_habit_periodicity(self):
        """
            Test creating a habit with an invalid periodicity value.
        """
        data = self.habit_data
        data['periodicity'] = 'sometimes'

        response = self.client.post(
            '/habits/create', data
        )

        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(Habit.objects.all().exists())
        self.assertEqual(response_data['periodicity'][0],
                         "Invalid value for 'periodicity'. Valid values are: daily, every_other_day, "
                         "every_third_day, every_fourth_day, every_fifth_day, every_sixth_day, weekly")







