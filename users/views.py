from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User
from users.serializers import RegistrationSerializer


class RegistrationApiView(generics.CreateAPIView):
    """
    API endpoint for user registration.

    This view allows users to register by providing their username, password, and Telegram ID.

    Attributes:
        permission_classes (tuple): The permission classes required to access this view.
        serializer_class (class): The serializer class for user registration.

    Example:
        To register a new user, make a POST request to this endpoint with the required data.
    """

    permission_classes = (AllowAny, )
    serializer_class = RegistrationSerializer

    def perform_create(self, serializer):
        User.objects.create_user(**serializer.validated_data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        message = ("You have been successfully registered! To start receiving habit notifications, "
                   "please go to the @rusanov_habit_bot and send the /start command.")

        return Response({'message': message}, status=status.HTTP_201_CREATED)




