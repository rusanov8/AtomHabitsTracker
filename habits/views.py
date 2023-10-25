from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.permissions import IsAuthenticated

from habits.models import Habit
from habits.paginators import HabitPaginator
from habits.permissions import IsOwner
from habits.serializers import HabitCreateUpdateSerializer, HabitListSerializer, HabitDetailSerializer


class HabitCreateView(generics.CreateAPIView):
    """
        API endpoint to create a new habit.

        Required permissions: User must be authenticated.

        Attributes:
            serializer_class (class): The serializer class for habit creation.
            permission_classes (tuple): The permission classes required to access this view.
        """
    serializer_class = HabitCreateUpdateSerializer
    permission_classes = (IsAuthenticated,)


class PublicHabitsListApiView(generics.ListAPIView):
    """
       API endpoint to retrieve a list of public habits.

       Required permissions: User must be authenticated.

       Attributes:
           serializer_class (class): The serializer class for listing habits.
           permission_classes (tuple): The permission classes required to access this view.
       """
    serializer_class = HabitListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
                Retrieve the list of public habits.

                Returns:
                    QuerySet: The queryset of public habits excluding those owned by the current user.
                """
        queryset = Habit.objects.filter(is_public=True).exclude(owner=self.request.user)
        return queryset


class OwnHabitsListApiView(generics.ListAPIView):
    """
        API endpoint to retrieve a list of habits owned by the authenticated user.

        Required permissions: User must be authenticated.

        Attributes:
            serializer_class (class): The serializer class for listing habits.
            pagination_class (class): The paginator class for paginating the list.
            permission_classes (tuple): The permission classes required to access this view.
        """
    serializer_class = HabitListSerializer
    pagination_class = HabitPaginator
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """
        Retrieve the list of habits owned by the authenticated user.

        Returns:
            QuerySet: The queryset of habits owned by the current user.
        """
        queryset = Habit.objects.filter(owner=self.request.user)
        if not queryset:
            return []
        return queryset


class HabitDetailView(generics.RetrieveAPIView):
    """
    API endpoint to retrieve the details of a specific habit.

    Required permissions: User must have appropriate permissions based on habit visibility (public or owner).

    Attributes:
        serializer_class (class): The serializer class for displaying habit details.
        queryset (QuerySet): The queryset of all habits.
    """
    serializer_class = HabitDetailSerializer
    queryset = Habit.objects.all()

    def get_permissions(self):

        try:
            habit = Habit.objects.get(pk=self.kwargs.get('pk'))
        except Habit.DoesNotExist:
            raise NotFound("Привычка не найдена")

        if habit.is_public:
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (IsOwner,)
        return (permission() for permission in permission_classes)


class HabitUpdateView(generics.UpdateAPIView):
    """
        API endpoint to update an existing habit.

        Required permissions: User must be the owner of the habit.

        Attributes:
            serializer_class (class): The serializer class for habit update.
            queryset (QuerySet): The queryset of all habits.
            permission_classes (tuple): The permission classes required to access this view.
        """
    serializer_class = HabitCreateUpdateSerializer
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)


class HabitDeleteView(generics.DestroyAPIView):
    """
      API endpoint to delete an existing habit.

      Required permissions: User must be the owner of the habit.

      Attributes:
          queryset (QuerySet): The queryset of all habits.
          permission_classes (tuple): The permission classes required to access this view.
      """
    queryset = Habit.objects.all()
    permission_classes = (IsOwner,)
