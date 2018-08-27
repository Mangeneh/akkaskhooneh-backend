from django.test import TestCase
from authentication.models import User
from string import ascii_letters
from random import choice

from rest_framework.test import APIClient


class EditProfileTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        self.password = 'sjkkensks'
        self.user.set_password(self.password)
        self.user.save()

        self.client.login(email=self.user.email, password=self.password)

    def test_true_edit_profile(self):
        data = {
            'bio': 'salam',
            'fullname': 'ali'
        }

        response = self.client.post("/auth/editprofile/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_edit_bio(self):
        data = {
            'bio': 'salamm'
        }

        response = self.client.post("/auth/editprofile/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_edit_name(self):
        data = {
            'fullname': 'ali'
        }
        response = self.client.post("/auth/editprofile/", data=data)
        self.assertEqual(response.status_code, 200)

    def test_edit_big_bio(self):
        data = {
            'bio': ''.join(choice(ascii_letters) for _ in range(301))
        }
        response = self.client.post("/auth/editprofile/", data=data)
        self.assertEqual(response.status_code, 400)
