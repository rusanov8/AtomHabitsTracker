from rest_framework.serializers import ValidationError


class TelegramIDValidator:
    """
       Validator for ensuring Telegram IDs start with '@'.
       This validator checks if a Telegram ID starts with the '@' symbol.
    """

    def __init__(self, field):
        self.field = field

    def __call__(self, value):
        tmp_value = dict(value).get(self.field)
        if not tmp_value.startswith('@'):
            raise ValidationError({"telegram_id": ["Telegram ID should start with the '@' symbol"]})



