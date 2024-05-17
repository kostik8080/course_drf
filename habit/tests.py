from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from habit.models import Habit
from users.models import User


class HabitTestCase(APITestCase):
    """Тесты для модели Habit"""

    def setUp(self):
        """Создание пользователя и привычки запись в базу"""
        self.user = User.objects.create(email='test@test.com')
        self.client.force_authenticate(user=self.user)
        self.habit = Habit.objects.create(
            user=self.user,
            place='test',
            time='21:00',
            action='сделать пробежку',
            period='Каждый день',
            time_to_complete='00:01:30',

        )
        self.habit2 = Habit.objects.create(
            user=self.user,
            place='test_1',
            time='21:00',
            action='просмотреть урок',
            period='Каждый день',
            time_to_complete='00:01:30',
            sign_pleasand_habit=True,
            public=True

        )

    def test_create_users(self):
        """Проверка создания привычки"""
        url = reverse('habit:habit_create')
        data = {
            'user': self.user.pk,
            'place': 'test2',
            'time': '22:00',
            'action': 'посмотреть урок',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Habit.objects.count(), 3)

        self.assertEqual(Habit.objects.get(id=1), self.habit)

    def test_update_habit(self):
        """Проверка обновления привычки"""
        url = reverse('habit:habit_update', args=[self.habit.pk])
        data = {
            'user': self.user.pk,
            'place': 'test3',
            'action': 'почитать книгу',
            'period': 'Каждый день',
            'time_to_complete': '00:01:50',

        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.habit.refresh_from_db()
        self.assertEqual(self.habit.place, 'test3')
        self.assertEqual(self.habit.action, 'почитать книгу')
        self.assertEqual(self.habit.period, 'Каждый день')
        self.assertEqual(
            self.habit.time_to_complete.strftime
            ('%H:%M:%S'),
            '00:01:50'
        )
        self.assertEqual(self.habit.public, False)

    def test_validation_plese_useful(self):
        """Проверка валидации при создании привычки"""
        url = reverse('habit:habit_create')
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,
            'award': 'Сделать отдых',
            'sign_pleasand_habit': True,
            # 'pleasant_habit': self.habit.id,

        }
        response = self.client.post(url, data)
        content = response.json()

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(content.get('non_field_errors'),
                         ['У приятной привычки'
                          ' не может быть вознаграждения'
                          ' или связанной привычки.'])
        url = reverse('habit:habit_update', args=[self.habit.pk])
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,
            'award': 'Сделать отдых',
            'sign_pleasand_habit': True,
            # 'pleasant_habit': self.habit.id,

        }
        response = self.client.put(url, data)
        content = response.json()
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(content.get('non_field_errors'),
                         ['У приятной привычки'
                          ' не может быть вознаграждения'
                          ' или связанной привычки.'])

    def test_validation_time(self):
        """Проверка валидации при создании привычки"""
        url = reverse('habit:habit_create')
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:02:30',
            'public': True,
            # 'award': 'Сделать отдых',
        }
        response = self.client.post(url, data)
        content = response.json()
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['Время выполнения '
             'не может быть больше 2 минут'])
        url = reverse(
            'habit:habit_update',
            args=[self.habit.pk])
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:02:30',
            'public': True,
            # 'award': 'Сделать отдых',
        }
        response = self.client.put(url, data)
        content = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['Время выполнения'
             ' не может быть больше 2 минут'])

    def test_related_sign_validator(self):
        """Проверка валидации при создании привычки"""
        url = reverse('habit:habit_create')
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,

            'sign_pleasand_habit': False,
            'pleasant_habit': self.habit.id,
        }
        response = self.client.post(url, data)
        content = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['В связанные привычки '
             'могут попадать только привычки '
             'с приятным признаком.'])
        url = reverse(
            'habit:habit_update',
            args=[self.habit.pk])
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,

            'sign_pleasand_habit': False,
            'pleasant_habit': self.habit.id,
        }
        response = self.client.put(url, data)
        content = response.json()
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['В связанные привычки могут '
             'попадать только привычки с приятным признаком.'])

    def test_good_sign_validator(self):
        """Проверка валидации при создании привычки"""
        url = reverse('habit:habit_create')
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,
            'sign_pleasand_habit': True,
            'pleasant_habit': self.habit2.id,
        }
        response = self.client.post(url, data)
        content = response.json()
        print(response.json())
        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['У приятной привычки'
             ' не может быть вознаграждения '
             'или связанной привычки.'])

        url = reverse(
            'habit:habit_update',
            args=[self.habit.pk])
        data = {
            'user': self.user.pk,
            'place': 'test4',
            'time': '22:00',
            'action': 'посмотреть лекцию',
            'period': 'Каждый день',
            'time_to_complete': '00:01:30',
            'public': True,
            'sign_pleasand_habit': True,
            'pleasant_habit': self.habit2.id,

        }
        response = self.client.put(url, data)
        content = response.json()

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )
        self.assertEqual(
            content.get('non_field_errors'),
            ['У приятной привычки'
             ' не может быть вознаграждения'
             ' или связанной привычки.'])

    def test_list_habit_public(self):
        """Проверка списка публичных привычек"""
        url = reverse('habit:habit_list_public')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            4)

    def test_list_habit_personal(self):
        """Проверка списка личных привычек"""
        url = reverse('habit:habit_list_personal')
        response = self.client.get(url)

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )
        self.assertEqual(
            len(response.data),
            4)

    def test_delete_habit(self):
        """Проверка удаления привычки"""
        url = reverse(
            'habit:habit_delete',
            args=[self.habit.pk])
        response = self.client.delete(url)
        self.assertEqual(
            response.status_code,
            status.HTTP_204_NO_CONTENT
        )
        self.assertEqual(
            Habit.objects.count(),
            1)
        with self.assertRaises(
                Habit.DoesNotExist):
            Habit.objects.get(
                id=1)
