from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from users.models import User


class UserTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email='test@test.com', password='12345')
        self.client.force_authenticate(user=self.user)

    def test_create_user(self):
        """
        Test creating a new user.
        """
        url = reverse('users:register')
        data = {

            'email': 'john@example.com',
            'password': '12345',

        }

        response = self.client.post(url, data)
        print(response.json())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_update_user(self):
        """
        Test updating a user.
        """
        url = reverse('users:user_profile', kwargs={'pk': self.user.pk})
        data = {
            'email': self.user.email,
            'password': self.user.password,
            'first_name': 'John',
            'last_name': 'Doe',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json()['first_name'], 'John')
        self.assertEqual(response.json()['last_name'], 'Doe')


