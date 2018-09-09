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

    def test_public_comment_post(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Comment.objects.filter(user=self.user1, post=post).count())

    def test_public_already_commented_post(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_public_comment_my_post_post(self):
        post = self.create_post(self.user1)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_private_comment_my_post_post(self):
        post = self.create_post(self.user1)
        self.to_private(self.user1)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_private_comment_post(self):
        post = self.create_post(self.user2)
        self.to_private(self.user2)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Comment.objects.filter(user=self.user1, post=post).count())

    def test_private_following_comment_post(self):
        post = self.create_post(self.user2)
        self.to_private(self.user2)
        Followers.objects.create(user=self.user1, following=self.user2)
        response = self.client.post("/social/comment/", {'post_id':post.id,'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(1, Comment.objects.filter(user=self.user1, post=post).count())

    def test_no_post_id_comment(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'content':'sks'})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Comment.objects.filter(user=self.user1, post=post).count())

    def test_no_content_comment(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Comment.objects.filter(user=self.user1, post=post).count())

    def test_empty_content_comment(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'content':'', 'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Comment.objects.filter(user=self.user1, post=post).count())

    def test_big_content_comment(self):
        post = self.create_post(self.user2)
        response = self.client.post("/social/comment/", {'content':''.join(choice(ascii_letters) for _ in range(1010)), 'post_id':post.id})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Comment.objects.filter(user=self.user1, post=post).count())
