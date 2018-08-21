from django.test import TestCase
from authentication.models.models import User
from authentication.utils import create_user, login_after_signup


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

    def test_login_after_signup(self):
        user = create_user(self.data)
        token = login_after_signup(user)
        data = {"token": token}
        response = self.client.post("/auth/token/verify/", data=data)
        self.assertEqual(response.status_code, 200)
