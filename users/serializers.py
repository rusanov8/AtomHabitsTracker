from rest_framework import serializers
from users.validators import TelegramIDValidator

from users.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for user registration.
    This serializer is used for creating a new user instance, including the required fields for registration.
    """

    class Meta:
        model = User
        fields = ('username', 'password', 'telegram_id')
        validators = [TelegramIDValidator(field='telegram_id')]

    # def create(self, validated_data):
    #     """
    #         Create and return a new user using the validated data.
    #     """
    #     return User.objects.create_user(**validated_data)
    #
