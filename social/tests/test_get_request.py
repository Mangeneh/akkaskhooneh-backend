from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class GetRequestTest(TestCase):
    def create(self, email, username, password):
        user = User.objects.create(email=email, username=username, password='')
        user.set_password(password)
        user.save()
        return user

    def setUp(self):
        self.password = 'sjkkensks'
        self.user1 = self.create('t@t.com', 'test', self.password)
        self.user2 = self.create('tt@tt.com', 'test2', self.password)
        self.client.login(email=self.user1.email, password=self.password)

    def test_has_request(self):
        Request.objects.create(requester=self.user2, requestee=self.user1)
        response = self.client.get("/social/followrequest/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_no_request(self):
        response = self.client.get("/social/followrequest/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_other_request(self):
        Request.objects.create(requester=self.user1, requestee=self.user2)
        response = self.client.get("/social/followrequest/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

