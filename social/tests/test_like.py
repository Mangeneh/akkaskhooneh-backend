from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request, Like
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

    def create_post(self, owner):
        post = Posts.objects.create(owner=owner, picture='1.png')
        return post

    def test_public_like_post(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Like.objects.filter(user=self.user1, post=post).count())

    def test_public_already_liked_post(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/like/", {'post_id':post.id})
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Like.objects.filter(user=self.user1, post=post).count())

    def test_public_like_my_post(self):
        post = self.create_post(self.user1)
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Like.objects.filter(user=self.user1, post=post).count())

    def test_public_like_my_private_post(self):
        post = self.create_post(self.user1)
        self.to_private(self.user1)
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Like.objects.filter(user=self.user1, post=post).count())


    def test_public_like_other_private_post(self):
        post = self.create_post(self.user2)
        self.to_private(self.user2)
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Like.objects.filter(user=self.user1, post=post).count())

    def test_public_like_other_private_following_post(self):
        post = self.create_post(self.user2)
        self.to_private(self.user2)
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.post("/social/like/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, Like.objects.filter(user=self.user1, post=post).count())

    def test_null_post_id_like(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/like/", {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Like.objects.filter(user=self.user1, post=post).count())
