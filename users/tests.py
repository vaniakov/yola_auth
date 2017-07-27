from django.test import TestCase
from users.serializers import User, UserSerializer


class UserSerializerTestCase(TestCase):

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
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertTrue(user.is_active)
        self.assertEqual(user.username, self.data2['username'])

    def test_instance_update(self):
        serializer = UserSerializer(self.user, {'first_name': 'First',
                                                'username': 'None'})
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.first_name, 'First')
        self.assertEqual(user.username, self.data1['username'])