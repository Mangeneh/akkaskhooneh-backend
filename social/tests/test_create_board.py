from random import choice
from string import ascii_letters
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from authentication.models import User
from social.models import Board


class CreateBoardTest(TestCase):
    def setUp(self):
        self.password = "fs98jidf"
        self.email = 't@t.com'
        self.username = 'test'
        self.user = User.objects.create_user(email=self.email,
                                             username=self.username,
                                             password=self.password)
        self.user.save()
        self.client.login(email=self.email, password=self.password)

    def test_true_create_board(self):
        response = self.client.post("/social/create-new-board/", data={'name': 'hello'})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        try:
            Board.objects.get(name='hello')
        except ObjectDoesNotExist as e:
            self.assertFalse(True, "board not added!")

    def test_empty_name(self):
        response = self.client.post("/social/create-new-board/", data={'name': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_name(self):
        response = self.client.post("/social/create-new-board/", data={'name': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_name(self):
        response = self.client.post("/social/create-new-board/", data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_big_name(self):
        big_name = ''.join(choice(ascii_letters) for _ in range(1000))
        response = self.client.post("/social/create-new-board/", data={'name': big_name})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
