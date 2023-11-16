from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitListAPIView,
    PublicHabitListAPIView,
    HabitCreateAPIView,
    HabitRetrieveAPIView,
    HabitUpdateAPIView,
    HabitDestroyeAPIView,
)

app_name = HabitConfig.name

urlpatterns = [
    path("", HabitListAPIView.as_view(), name="habit_list"),
    path("public/", PublicHabitListAPIView.as_view(), name="habit_public"),
    path("create/", HabitCreateAPIView.as_view(), name="habit_create"),
    path("<int:pk>/", HabitRetrieveAPIView.as_view(), name="habit_detail"),
    path("update/<int:pk>/", HabitUpdateAPIView.as_view(), name="habit_update"),
    path("delete/<int:pk>/", HabitDestroyeAPIView.as_view(), name="habit_delete"),
]
