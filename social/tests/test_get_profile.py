from django.test import TestCase
from authentication.models import User
from rest_framework import status

class GetProfileTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        password = 'sjkkensks'
        self.user.set_password(password)
        self.user.save()
        self.client.login(email=self.user.email, password=password)

    def test_true_get_my_profile(self):
        response = self.client.get("/social/profile/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_true_get_other_profile(self):
        response = self.client.get("/social/profile/test")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_get_other_profile(self):
        response = self.client.get("/social/profile/testsksksnosnxsldln")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

