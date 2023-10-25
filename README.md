# AtomHabitTracker

AtomHabitTracker is an application for tracking and managing habits and tasks. This web application allows users to create, edit, and track their habits, as well as interact with a Telegram bot for habit management.

## Installation

Before using AtomHabitTracker, make sure you have Python 3.6+ and [virtualenv](https://pypi.org/project/virtualenv) installed. Follow these steps:

1. Clone the repository:
https://github.com/rusanov8/AtomHabitsTracker.git


2. Navigate to the project directory: 
cd atom-habit-tracker


3. Create a virtual environment:
virtualenv venv


4. Activate the virtual environment:

- For Windows:

  ```
  venv\Scripts\activate
  ```

- For macOS and Linux:

  ```
  source venv/bin/activate
  ```

5. Install dependencies:
  ```
  pip install -r requirements.txt
  ```

6. Apply migrations:
python manage.py migrate


7. Start the application:
python manage.py runserver


8. You can now open AtomHabitTracker in your web browser at `http://127.0.0.1:8000/`.

## Running the AtomHabitTracker Telegram Bot

To run the AtomHabitTracker Telegram bot used for habit management, follow these steps:

1. With the virtual environment activated, run the following command:
python telegram_bot.py
2. The bot will be available in Telegram as `@atom_habit_bot`. Start a chat with the bot and execute the `/start` command. The bot will save your `chat_id` in the database and begin sending notifications.

## Additional Information

- [Django](https://www.djangoproject.com/): The web framework used for the web portion of the application.
- [Django REST framework](https://www.django-rest-framework.org/): A library for creating RESTful APIs in Django.
- [python-telegram-bot](https://python-telegram-bot.readthedocs.io/en/stable/): A library for creating Telegram bots.

## Author

* [Rusanov Egor]
