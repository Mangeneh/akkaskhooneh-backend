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
        self.user1 = self.create('t@t.com', 'dsfas', self.password)
        self.user2 = self.create('tt@tt.com', 'skakfe', self.password)
        self.client.login(email=self.user1.email, password=self.password)

    def set_fullname(self, user, fullname):
        user.fullname = fullname
        user.save()


    def test_username_search(self):
        response = self.client.get("/social/search/user/?search=a")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_username_search2(self):
        response = self.client.get("/social/search/user/?search=fa")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_username_fullname_search(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=e")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_username_fullname_search2(self):
        self.set_fullname(self.user1, 'ds')
        response = self.client.get("/social/search/user/?search=e")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_username_fullname_search3(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_username_fullname_search4(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=kdkse")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 0)

    def test_username_fullname_search5(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=s e")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)

    def test_username_fullname_search6(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=sj ekd")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 1)

    def test_username_fullname_search6(self):
        self.set_fullname(self.user1, 'esjs')
        response = self.client.get("/social/search/user/?search=dsf fe")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data.get('count'), 2)