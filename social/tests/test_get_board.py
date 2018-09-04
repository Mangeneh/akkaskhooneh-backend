from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from authentication.models import User
from social.models import Board, Followers, Posts, BoardContains
import io
from PIL import Image


class GetBoardTest(TestCase):

    def create_user(self, username, email, password, **kwargs):
        user = User.objects.create_user(email=email,
                                        username=username,
                                        password=password,
                                        **kwargs)
        user.save()
        return user

    def setUp(self):
        self.user1 = self.create_user(username="test1", email="t1@t1@.com", password="yhes11")
        self.user2 = self.create_user(username="test2", email="t2@t2.com", password="yhes22", is_private=True)
        self.user3 = self.create_user(username="test3", email="t3@t3.com", password="yhes33", is_private=True)
        self.user4 = self.create_user(username="test4", email="t4@t4.com", password="yhes44")

        self.board1 = Board.objects.create(owner=self.user1, name='b1')
        self.board2 = Board.objects.create(owner=self.user2, name='b2')
        self.board3 = Board.objects.create(owner=self.user3, name='b3')
        self.board4 = Board.objects.create(owner=self.user4, name='b4')

        self.flw = Followers.objects.create(user=self.user1, following=self.user2)

        self.client.login(email="t1@t1@.com", password="yhes11")

    def test_get_boards_my_detail(self):
        response = self.client.get("/social/boardsdetails/1/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_boards_flw_detail(self):
        response = self.client.get("/social/boardsdetails/2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_boards_not_flw_detail(self):
        response = self.client.get("/social/boardsdetails/3/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_boards_pub_detail(self):
        response = self.client.get("/social/boardsdetails/4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_boards_my(self):
        response = self.client.get("/social/boards/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_boards_flw(self):
        response = self.client.get("/social/boards/test2/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_boards_not_flw(self):
        response = self.client.get("/social/boards/test3/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_boards_pub(self):
        response = self.client.get("/social/boards/test4/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

