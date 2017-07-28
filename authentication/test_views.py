from django.test import TestCase
from django.urls import reverse
from users.serializers import User, UserSerializer
from rest_framework.test import APIClient
from rest_framework import status


class UserViewSetTests(TestCase):

    def setUp(self):
        self.email = 'jpueblo@example.com'
        self.username = 'jpueblo'
        self.password = 'password'
        self.user = User.objects.create_user(email=self.email,
                                        username=self.username,
                                        password=self.password)
        self.data = {
            'email': self.email,
            'password': self.password,
            'username': self.username
        }

    def test_get_user_list_forbidden(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.get('/api/v1/users/', format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_edit_user_forbidden(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/v1/users/1/', data={'first_name': 'First'},
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_user_forbidden(self):
        client = APIClient(enforce_csrf_checks=True)
        response = client.post('/api/v1/users/', data=self.data,
                               format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_list_session_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username=self.username, password=self.password)
        response = client.get(reverse('users:user-list'), format='json')
        user_data = response.data[0]
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(user_data['email'], self.data['email'])

    def test_get_user_inst_session_auth(self):
        client = APIClient(enforce_csrf_checks=True)
        client.login(username=self.username, password=self.password)
        response = client.get(reverse('users:user-detail',
                                       args=(self.user.id,)), format='json')
        user_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['email'], self.data['email'])

    def test_get_another_user_inst(self):
        user2 = User.objects.create_user(username='test2', email='test2@gmail.com', password='password2')
        client = APIClient(enforce_csrf_checks=True)
        client.login(username=self.username, password=self.password)
        response = client.get(reverse('users:user-detail',
                                       args=(user2.id,)), format='json')
        user_data = response.data
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['email'], 'test2@gmail.com')

    def test_update_user(self):
        client = APIClient()
        client.login(username=self.username, password=self.password)

        url = reverse('users:user-detail', args=(self.user.id,))
        data = {'first_name':'First', 'last_name': 'Second'}

        response = client.patch(url, data)
        user_data = response.data

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(user_data['first_name'], 'First')
        self.assertEqual(user_data['last_name'], 'Second')


