from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class UnfollowRequestTest(TestCase):
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

    def follow(self, user1, user2):
        Followers.objects.create(user=user1, following=user2)

    def test_public_unfollow(self):
        self.follow(self.user1, self.user2)
        response = self.client.post("/social/unfollow/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_private_unfollow(self):
        self.to_private(self.user2)
        self.follow(self.user1, self.user2)
        response = self.client.post("/social/unfollow/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_wrong_username(self):
        self.follow(self.user1, self.user2)
        response = self.client.post("/social/unfollow/", {'username':'test22'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(1, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_not_following_unfollow(self):
        response = self.client.post("/social/unfollow/", {'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Followers.objects.filter(user=self.user1, following=self.user2).count())

    def test_no_username(self):
        self.follow(self.user1, self.user2)
        response = self.client.post("/social/unfollow/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Followers.objects.filter(user=self.user1, following=self.user2).count())
