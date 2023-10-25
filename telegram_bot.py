import logging
import os

import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from users.models import User

from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler
from asgiref.sync import sync_to_async


class TelegramBot:
    """
        TelegramBot class for registering users' chat IDs.

        This class is designed to handle the registration of users by processing the "start" command
        in the Telegram chat, capturing the user's chat ID, and saving it to the associated user.
    """

    METHOD_NAME = 'sendMessage'

    def __init__(self):
        self.access_token = os.getenv('TG_ACCESS_TOKEN')
        if not self.access_token:
            raise ValueError("Telegram access token is not provided.")

        self.setup_logging()
        self.setup_handlers()

    def setup_logging(self):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )

    def setup_handlers(self):
        application = ApplicationBuilder().token(self.access_token).build()
        start_handler = CommandHandler('start', self.start)
        application.add_handler(start_handler)
        application.run_polling()

    @sync_to_async
    def get_user(self, telegram_id):
        try:
            return User.objects.get(telegram_id=telegram_id)
        except User.DoesNotExist:
            return None

    @sync_to_async
    def save_user(self, user):
        user.save()

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        telegram_id = f'@{update.message.from_user.username}'
        chat_id = update.effective_chat.id

        user = await self.get_user(telegram_id)
        if user:
            user.chat_id = chat_id
            await self.save_user(user)
            await context.bot.send_message(
                chat_id=chat_id,
                text="Hello! My name is AtomHabitsBot. I will help you build new habits!"
            )
        else:
            await context.bot.send_message(chat_id=chat_id, text='Registration failed.')


if __name__ == '__main__':
    bot = TelegramBot()
