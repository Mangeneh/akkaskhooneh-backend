from random import choice
from string import ascii_letters
from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request, Comment
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

    def create_comment(self, user, post):
        return Comment.objects.create(user=user, post=post)

    def test_public_get_comments_post(self):
        post = self.create_post(self.user2)
        comment = self.create_comment(self.user2, post)
        response = self.client.get("/social/comment/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data.get('count'))

    def test_public_get_my_comments_post(self):
        post = self.create_post(self.user1)
        comment = self.create_comment(self.user1, post)
        response = self.client.get("/social/comment/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data.get('count'))

    def test_private_get_my_comments_post(self):
        self.to_private(self.user1)
        post = self.create_post(self.user1)
        comment = self.create_comment(self.user1, post)
        response = self.client.get("/social/comment/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data.get('count'))

    def test_private_get_comments_post(self):
        self.to_private(self.user2)
        post = self.create_post(self.user2)
        comment = self.create_comment(self.user2, post)
        response = self.client.get("/social/comment/1/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_private_following_get_comments_post(self):
        self.to_private(self.user2)
        Followers.objects.create(user=self.user1, following=self.user2)
        post = self.create_post(self.user2)
        comment = self.create_comment(self.user2, post)
        response = self.client.get("/social/comment/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(1, response.data.get('count'))

