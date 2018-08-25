from django.test import TestCase
from authentication.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        self.password = 'sjkkensks'
        self.user.set_password(self.password)
        self.user.save()

        self.data = {
            'email': self.user.email,
            'password': self.password
        }

    def check_status_login(self, data, status):
        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, status)

    def test_login(self):
        password = self.password
        data = self.data
        self.check_status_login(data, 201)

        data['password'] = 'a'
        self.check_status_login(data, 400)

        data['password'] = password
        data['email'] = 'a@a.com'
        self.check_status_login(data, 400)

        data['password'] = data['email'] = None
        self.check_status_login(data, 400)

    def test_verify(self):
        data = self.data

        response = self.client.post("/auth/login/", data=data)
        token = response.json()['access']

        data = {
            'token':token
        }

        verify_response = self.client.post("/auth/token/verify/", data=data)

        self.assertEqual(verify_response.status_code, 200)

    def test_signup(self):
        response = self.client.post("/auth/register/", data=self.data)
        self.assertEqual(response.status_code, 400)

        data = {
            'username': 'testewlw',
            'email': 'test@t.com',
            'password': '1234'
        }

        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 201)
