from django.test import TestCase
from authentication.models import User
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

