# apps/user/tests/test_user.py

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from apps.user.config.models import User

class UserTests(APITestCase):

    def test_register_user(self):
        url = reverse('user-register')
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['username'], 'testuser')

    def test_update_profile(self):
        user = User.objects.create_user(username='testuser', email='test@example.com', password='password123')
        self.client.login(username='testuser', password='password123')
        url = reverse('user-profile', kwargs={'pk': user.id})
        data = {'profile': {'first_name': 'John', 'last_name': 'Doe'}}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['profile']['first_name'], 'John')
