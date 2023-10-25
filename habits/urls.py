from django.urls import path

from habits.apps import HabitsConfig
from habits.views import (HabitCreateView, PublicHabitsListApiView, HabitDetailView,
                          HabitUpdateView, HabitDeleteView, OwnHabitsListApiView)

app_name = HabitsConfig.name

urlpatterns = [
    path('habits/create', HabitCreateView.as_view(), name='habit-create'),
    path('habits', OwnHabitsListApiView.as_view(), name='own-habit-list'),

    path('habits/public', PublicHabitsListApiView.as_view(), name='public-habit-list'),

    path('habits/<int:pk>', HabitDetailView.as_view(), name='habit-detail'),
    path('habits/edit/<int:pk>', HabitUpdateView.as_view(), name='habit-list'),
    path('habits/delete/<int:pk>', HabitDeleteView.as_view(), name='habit-list')

]
