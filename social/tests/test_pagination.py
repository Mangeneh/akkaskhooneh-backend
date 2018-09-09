from django.test import TestCase
from authentication.models import User
from social.models import Followers
from rest_framework import status

class PaginationTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        password = 'sjkkensks'
        self.user.set_password(password)
        self.user.save()
        self.client.login(email=self.user.email, password=password)

    def test_true_get_my_posts(self):
        response = self.client.get("/social/pictures/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_true_get_other_posts(self):
        response = self.client.get("/social/pictures/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_get_other_posts(self):
        response = self.client.get("/social/pictures/testsksksnosnxsldln/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


    def test_get_my_private_posts(self):
        self.user.is_private = True
        self.user.save()
        response = self.client.get("/social/pictures/test/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_public_posts(self):
        user = User.objects.create(email='tt@tt.com', username='testt', password='')
        password = 'sjkkensks'
        user.set_password(password)
        user.save()
        response = self.client.get("/social/pictures/testt/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_other_private_posts(self):
        user = User.objects.create(email='tt@tt.com', username='testt', password='')
        password = 'sjkkensks'
        user.set_password(password)
        user.is_private = True
        user.save()
        response = self.client.get("/social/pictures/testt/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_other_private_following_posts(self):
        user = User.objects.create(email='tt@tt.com', username='testt', password='')
        password = 'sjkkensks'
        user.set_password(password)
        user.is_private = True
        user.save()
        Followers.objects.create(user=self.user, following=user)
        response = self.client.get("/social/pictures/testt/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
