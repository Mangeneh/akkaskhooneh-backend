from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from authentication.models import User


class UserTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        self.password = 'test'
        self.user.set_password(self.password)
        self.user.save()

    def test_change_password_success(self):
        new_password = 'testTEST1234'
        post_data = {
            'old_password': self.password,
            'password': new_password,
            'repeat_password': new_password,
        }
        login_data = {
            'email': 't@t.com',
            'password': 'test'

        }
        login_response = self.client.post("/auth/login/", data=login_data)
        access_token = login_response.json().get('access')
        auth = 'Bearer ' + access_token

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=auth)

        change_password_response = client.put("/auth/changepassword/", data=post_data)
        self.assertEqual(change_password_response.status_code, status.HTTP_200_OK)

    def test_change_password_wrong_old_password(self):
        new_password = 'testTEST1234'
        post_data = {
            'old_password': "wghjk",
            'password': new_password,
            'repeat_password': new_password,
        }
        login_data = {
            'email': 't@t.com',
            'password': 'test'
        }
        login_response = self.client.post("/auth/login/", data=login_data)
        access_token = login_response.json().get('access')
        auth = 'Bearer ' + access_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=auth)
        change_password_response = client.put("/auth/changepassword/", data=post_data)
        self.assertEqual(change_password_response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_password_weak_new_password(self):
        new_password = '44'
        post_data = {
            'old_password': "wghjk",
            'password': new_password,
            'repeat_password': new_password,
        }
        login_data = {
            'email': 't@t.com',
            'password': 'test'
        }
        login_response = self.client.post("/auth/login/", data=login_data)
        access_token = login_response.json().get('access')
        auth = 'Bearer ' + access_token
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION=auth)
        change_password_response = client.put("/auth/changepassword/", data=post_data)
        self.assertEqual(change_password_response.status_code, status.HTTP_400_BAD_REQUEST)
