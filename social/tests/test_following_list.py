from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class GetFollowingTest(TestCase):
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

    def test_has_follower(self):
        Followers.objects.create(user=self.user2, following=self.user1)
        response = self.client.get("/social/following/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_no_follower(self):
        response = self.client.get("/social/following/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_has_following(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.get("/social/following/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_wrong_username(self):
        Followers.objects.create(user=self.user2, following=self.user1)
        response = self.client.get("/social/following/tesskskst/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_public_user_follower(self):
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.get("/social/following/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_private_user_follower(self):
        self.user2.is_private = True
        self.user2.save()
        response = self.client.get("/social/following/test2/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_private_user_following_follower(self):
        self.user2.is_private = True
        self.user2.save()
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.get("/social/following/test2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)




