from django.test import TestCase
from users.serializers import User, UserSerializer
from rest_framework.test import APIClient
from rest_framework import status


class UserSerializerTests(TestCase):

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

    def test_serialization(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data.get('username'), 'test')
        self.assertEqual(data.get('email'), 'test@gmail.com')
        self.assertIsNone(data.get('password', None))

    def test_deserialization(self):
        serializer = UserSerializer(data=self.data2)
        is_valid = serializer.is_valid()
        user = serializer.save()
        self.assertTrue(is_valid)
        self.assertTrue(user.is_active)
        self.assertEqual(user.username, self.data2['username'])

    def test_instance_update(self):
        serializer = UserSerializer(self.user, {'first_name': 'First',
                                                'username': 'None'})
        is_valid = serializer.is_valid()
        user = serializer.save()
        self.assertTrue(is_valid)
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.username, self.data1['username'])


class UserViewSetTests(TestCase):

    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.password = 'password'
        user = User.objects.create(email=self.email)
        user.set_password(self.password)
        user.save()
        self.user = user

        self.data = {
            'email': self.email,
            'password': self.password
        }

    def test_get_user_list_without_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.get('/api/v1/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_user_without_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/v1/users/1/', data={'first_name': 'First'},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_without_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/v1/users/', data=self.data,
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def _test_get_user_list(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.get('/api/v1/users/', format='json')
        user_data = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(user_data['email'], self.data['email'])

    def _test_get_user_inst(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.get('/api/v1/users/1/', format='json')
        user_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['email'], self.data['email'])