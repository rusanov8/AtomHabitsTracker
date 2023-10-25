import requests
import os
from dotenv import load_dotenv


load_dotenv()

TG_ACCESS_TOKEN = os.getenv('TG_ACCESS_TOKEN')
METHOD_NAME = 'sendMessage'


def telegram_bot(chat_id, text):
    """
    Send a message via a Telegram bot.
    This function sends a text message to a specific Telegram chat using a Telegram bot API.
    """

    api_url = f'https://api.telegram.org/bot{TG_ACCESS_TOKEN}/{METHOD_NAME}'

    data = {
        'chat_id': chat_id,
        'text': text
    }

    try:
        response = requests.post(url=api_url, params=data)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f'Error while sending a message via Telegram: {e}')

