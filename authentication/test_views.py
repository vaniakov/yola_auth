from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class RegisterViewTests(TestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.password = '$uper_$trong_p@$$'
        self.week_password = 'password'

        self.data = {
            'email': self.email,
            'password': self.password,
        }

    def test_register_valid_data(self):
        client = APIClient()
        response = client.post('/api/v1/register/', self.data, format='json')
        key = response.data.get('key')
        db_key_exists = Token.objects.filter(key=key).exists()

        self.assertTrue(db_key_exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('key' in response.data)

    def test_register_existent_user(self):
        User.objects.create_user(**self.data)
        client = APIClient()
        response = client.post('/api/v1/register/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_week_password(self):
        client = APIClient()
        response = client.post('/api/v1/register/', {'email': self.email,
                                                     'password': self.week_password},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class LoginViewTests(TestCase):
    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.password = '$uper_$trong_p@$$'
        self.week_password = 'password'

        self.data = {
            'email': self.email,
            'password': self.password,
        }

    def test_register_valid_data(self):
        client = APIClient()
        response = client.post('/api/v1/register/', self.data, format='json')
        key = response.data.get('key')
        db_key_exists = Token.objects.filter(key=key).exists()

        self.assertTrue(db_key_exists)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue('key' in response.data)

    def test_register_existent_user(self):
        User.objects.create_user(**self.data)
        client = APIClient()
        response = client.post('/api/v1/register/', self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_week_password(self):
        client = APIClient()
        response = client.post('/api/v1/register/', {'email': self.email,
                                                     'password': self.week_password},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)