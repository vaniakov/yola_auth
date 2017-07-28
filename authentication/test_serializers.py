from django.test import TestCase

from rest_framework.test import APIClient
from rest_framework import status

from authentication.serializers import RegisterSerializer, LoginSerializer
from users.models import User


class RegisterSerializerTests(TestCase):

    def setUp(self):
        self.data1 = {
            'username': 'test',
            'email': 'test@gmail.com',
            'password': 'secret_123'
        }
        self.data2 = {
            'username': 'test2',
            'email': 'test2@gmail.com',
            'password': 'secret_123'
        }
        self.user = User.objects.create(**self.data1)

    def tearDown(self):
        self.user.delete()

    def test_valid_data(self):
        serializer = RegisterSerializer(data=self.data2)
        is_valid = serializer.is_valid()
        user = serializer.save()
        self.assertTrue(is_valid)
        self.assertTrue(user.is_active)
        self.assertEqual(user.username, self.data2['username'])

    def test_user_already_exists(self):
        serializer = RegisterSerializer(data=self.data1)
        is_valid = serializer.is_valid()
        with self.assertRaises(ValueError):
            user = serializer.save()
        self.assertFalse(is_valid)


