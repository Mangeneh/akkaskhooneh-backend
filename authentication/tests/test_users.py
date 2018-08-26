from django.test import TestCase
from authentication.models import User
from string import ascii_letters
from random import choice

from rest_framework.test import APIClient


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
        response = self.client.post("/auth/login/", data=self.data)
        self.token = response.json()['access']

    def check_status_login(self, data, status):
        response = self.client.post("/auth/login/", data=data)
        self.assertEqual(response.status_code, status)

    def test_true_login(self):
        self.check_status_login(self.data, 200)

    def test_wrong_password_login(self):
        data = self.data
        data['password'] = 'a'
        self.check_status_login(data, 400)

    def test_wrong_email_login(self):
        data = self.data
        data['email'] = 'a@a.com'
        self.check_status_login(data, 400)

    def test_null_email_and_password_login(self):
        data = self.data
        data['password'] = data['email'] = None
        self.check_status_login(data, 400)

    def test_big_email_login(self):
        data = self.data
        for i in range(100):
            data['email'] = choice(ascii_letters) + data['email']
        self.check_status_login(data, 400)

    def test_big_password_login(self):
        data = self.data
        for i in range(100):
            data['password'] = choice(ascii_letters) + data['password']
        self.check_status_login(data, 400)

    def test_verify(self):
        verify_response = self.client.post("/auth/token/verify/", data={'token': self.token})
        self.assertEqual(verify_response.status_code, 200)

    def test_unique_email_register(self):
        response = self.client.post("/auth/register/", data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_unique_username_register(self):
        data = self.data
        data['email'] = 'test@t.com'
        response = self.client.post("/auth/register/", data=self.data)
        self.assertEqual(response.status_code, 400)

    def test_wrong_email_format_register(self):
        data = {
            'username': 'testewjlw',
            'email': 'test',
            'password': '1234@@@@'
        }

        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 400)

    def test_true_register(self):
        data = {
            'username': 'testewlw',
            'email': 'test@t.com',
            'password': '1234@@@@'
        }

        response = self.client.post("/auth/register/", data=data)
        self.assertEqual(response.status_code, 201)
