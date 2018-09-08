from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class FollowRequestTest(TestCase):
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

    def to_private(self, user):
        user.is_private = True
        user.save()

    def test_public_request(self):
        response = self.client.post("/social/request/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_private_request(self):
        self.to_private(self.user2)
        response = self.client.post("/social/request/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Request.objects.filter(requester=self.user1, requestee=self.user2).count())

    def test_public_followed_request(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.post("/social/request/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_private_requested_request(self):
        Request.objects.create(requester=self.user1, requestee=self.user2)
        self.to_private(self.user2)
        response = self.client.post("/social/request/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Request.objects.filter(requester=self.user1, requestee=self.user2).count())

    def test_private_followed_request(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        self.to_private(self.user2)
        response = self.client.post("/social/request/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_no_usename_request(self):
        response = self.client.post("/social/request/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_username_request(self):
        response = self.client.post("/social/request/", {'username':'test2skak'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_empty_username_request(self):
        response = self.client.post("/social/request/", {'username':''})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_follow_me_request(self):
        response = self.client.post("/social/request/", {'username':'test'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)





