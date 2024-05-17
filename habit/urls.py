from django.urls import path

from habit.apps import HabitConfig
from habit.views import (
    HabitListAPIView,
    HabitPersoneAPIView,
    HabitCreateAPIView,
    HabitUpdateAPIView,
    HabitDeleteAPIView)

app_name = HabitConfig.name

urlpatterns = [
    path('', HabitListAPIView.as_view(),
         name='habit_list_public'),
    path('habit/list_personal/',
         HabitPersoneAPIView.as_view(),
         name='habit_list_personal'),
    path('habit/create/',
         HabitCreateAPIView.as_view(),
         name='habit_create'),
    path('habit/update/<int:pk>/',
         HabitUpdateAPIView.as_view(),
         name='habit_update'),
    path('habit/delete/<int:pk>/',
         HabitDeleteAPIView.as_view(),
         name='habit_delete'),

]
