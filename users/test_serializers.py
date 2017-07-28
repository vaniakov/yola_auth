from django.test import TestCase
from django.contrib.auth import get_user_model

from users.serializers import UserSerializer

User = get_user_model()


class UserSerializerTests(TestCase):

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

    def test_serialization(self):
        serializer = UserSerializer(self.user)
        data = serializer.data
        self.assertEqual(data.get('email'), 'test@gmail.com')
        self.assertIsNone(data.get('password', None))

    def test_deserialization(self):
        serializer = UserSerializer(data=self.data2)
        is_valid = serializer.is_valid()
        user = serializer.save()
        self.assertTrue(is_valid)
        self.assertTrue(user.is_active)
        self.assertEqual(user.email, self.data2['email'])

    def test_instance_update(self):
        serializer = UserSerializer(self.user, {'first_name': 'First',
                                                'last_name': 'Last'},
                                    partial=True)
        is_valid = serializer.is_valid()
        user = serializer.save()

        self.assertTrue(is_valid)
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.email, self.data1['email'])


