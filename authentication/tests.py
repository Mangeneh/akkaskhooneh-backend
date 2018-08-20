from django.test import TestCase
from authentication.models import User
from authentication.utils import create_user


class UserTestCase(TestCase):
    def setUp(self):
        self.data = '''
        {
            "username": "kamyab",
            "password": "1",
            "email": "kamyab@kamyab.com"
        }
        '''

    def test_create_user(self):
        user = create_user(self.data)
        self.assertEqual(user, User.objects.first())
