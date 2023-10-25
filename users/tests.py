from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User

class UserTestCase(APITestCase):
    """
        Test cases for user registration.
    """

    def setUp(self):
        """
            Set up data for each test case.
        """

        self.data = {
            "username": "testuser",
            "password": "testpassword",
            "telegram_id": "@testtelegramid"
        }

        self.response_message = ("You have been successfully registered! To start receiving habit notifications, "
                                 "please go to the @rusanov_habit_bot and send the /start command.")

    def test_create_user(self):
        """
            Test user creation with valid data.
        """

        response = self.client.post(
            '/users/create', self.data
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(response.data['message'], self.response_message)

        self.assertTrue(User.objects.all().exists())

        self.assertIsNotNone(User.objects.get(username=self.data['username']))


    def test_create_user_with_invalid_telegram_id(self):
        """
            Test user creation with an invalid Telegram ID.
        """

        invalid_data = {
            "username": "testuser",
            "password": "testpassword",
            "telegram_id": "testtelegramid"
        }

        response = self.client.post(
            '/users/create', invalid_data
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertEqual(response.data["telegram_id"][0], "Telegram ID should start with the '@' symbol")







