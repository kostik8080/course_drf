
from rest_framework.generics import (
    ListAPIView,
    CreateAPIView,
    UpdateAPIView,
    DestroyAPIView)
from rest_framework.permissions import IsAuthenticated

from habit.models import Habit
from habit.paginators import HabitPagination
from habit.permissions import IsOwner
from habit.serializers import HabitSerializer


class HabitListAPIView(ListAPIView):
    """Список привычек которые опубликованы"""
    serializer_class = HabitSerializer
    queryset = Habit.objects.filter(public=True)
    pagination_class = HabitPagination


class HabitPersoneAPIView(ListAPIView):
    """Список привычек которые принадлежат пользователю"""
    serializer_class = HabitSerializer
    pagination_class = HabitPagination
    permission_classes = [IsOwner]

    def get_queryset(self):
        queryset = Habit.objects.filter(user=self.request.user)
        return queryset


class HabitCreateAPIView(CreateAPIView):
    serializer_class = HabitSerializer

    def perform_create(self, serializer):
        """
        Создание пользователя по умодчанию кто авторизован.
        """
        habit = serializer.save()
        habit.user = self.request.user
        habit.save()


class HabitUpdateAPIView(UpdateAPIView):
    serializer_class = HabitSerializer
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated & IsOwner]


class HabitDeleteAPIView(DestroyAPIView):
    queryset = Habit.objects.all()
    permission_classes = [IsAuthenticated & IsOwner]
