from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers
from rest_framework import status

class FeedTest(TestCase):
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

    def test_has_follower_feed(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        post = Posts.objects.create(owner=self.user2, picture='1.png')
        response = self.client.get("/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_no_follower_post_feed(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        post = Posts.objects.create(owner=self.user1, picture='1.png')
        response = self.client.get("/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_has_following_feed(self):
        Followers.objects.create(user=self.user2, following=self.user1)
        post = Posts.objects.create(owner=self.user2, picture='1.png')
        response = self.client.get("/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_no_follower_feed(self):
        post = Posts.objects.create(owner=self.user2, picture='1.png')
        response = self.client.get("/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_no_post_feed(self):
        Followers.objects.create(user=self.user2, following=self.user1)
        response = self.client.get("/social/feed/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

