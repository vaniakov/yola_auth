from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework import exceptions

from authentication.serializers import RegisterSerializer, LoginSerializer

User = get_user_model()


class RegisterSerializerTests(TestCase):

    def setUp(self):
        self.data1 = {
            'email': 'test@gmail.com',
            'password': 'secret_123'
        }
        self.data2 = {
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
        self.assertEqual(user.email, self.data2['email'])

    def test_user_already_exists(self):
        serializer = RegisterSerializer(data=self.data1)
        is_valid = serializer.is_valid()
        with self.assertRaises(ValueError):
            serializer.save()
        self.assertFalse(is_valid)

    def test_no_email(self):
        del self.data2['email']
        serializer = RegisterSerializer(data=self.data2)
        is_valid = serializer.is_valid()
        with self.assertRaises(ValueError):
            serializer.save()
        self.assertFalse(is_valid)

    def test_no_password(self):
        del self.data2['password']
        serializer = RegisterSerializer(data=self.data2)
        is_valid = serializer.is_valid()
        with self.assertRaises(ValueError):
            serializer.save()
        self.assertFalse(is_valid)


class LoginSerializerTests(TestCase):

    def setUp(self):
        self.data1 = {
            'email': 'test@gmail.com',
            'password': 'secret_123'
        }
        self.data2 = {
            'email': 'test2@gmail.com',
            'password': 'secret_123'
        }
        self.user = User.objects.create_user(**self.data1)

    def tearDown(self):
        self.user.delete()

    def test_valid_data(self):
        serializer = LoginSerializer(data=self.data1)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)

    def test_user_is_not_exists(self):
        serializer = LoginSerializer(data=self.data2)
        with self.assertRaises(exceptions.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_email(self):
        del self.data1['email']
        serializer = LoginSerializer(data=self.data1)
        with self.assertRaises(exceptions.ValidationError):
            serializer.is_valid(raise_exception=True)

    def test_no_password(self):
        del self.data1['password']
        serializer = LoginSerializer(data=self.data1)
        with self.assertRaises(exceptions.ValidationError):
            serializer.is_valid(raise_exception=True)
