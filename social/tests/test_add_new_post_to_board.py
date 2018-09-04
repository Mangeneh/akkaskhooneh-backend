from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from authentication.models import User
from social.models import Board, Followers, Posts, BoardContains
import io
from PIL import Image


class AddPostToBoardTest(TestCase):

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

        self.post1 = Posts.objects.create(owner=self.user1, picture="1.png")
        self.post2 = Posts.objects.create(owner=self.user2, picture="2.png")
        self.post3 = Posts.objects.create(owner=self.user3, picture="3.png")
        self.post4 = Posts.objects.create(owner=self.user4, picture="4.png")

        self.board1 = Board.objects.create(owner=self.user1, name='b1')
        self.board2 = Board.objects.create(owner=self.user2, name='b2')
        self.board3 = Board.objects.create(owner=self.user3, name='b3')
        self.board4 = Board.objects.create(owner=self.user4, name='b4')

        self.flw = Followers.objects.create(user=self.user1, following=self.user2)

        self.client.login(email="t1@t1@.com", password="yhes11")

    def test_add_my_post_to_my_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 1,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            BoardContains.objects.get(board=1, post=1)
        except ObjectDoesNotExist as e:
            self.assertFalse(True, "post not added!")

    def test_add_public_post_to_my_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 4,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            BoardContains.objects.get(board=1, post=4)
        except ObjectDoesNotExist as e:
            self.assertFalse(True, "post not added!")

    def test_add_flw_post_to_my_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 2,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            BoardContains.objects.get(board=1, post=2)
        except ObjectDoesNotExist as e:
            self.assertFalse(True, "post not added!")

    def test_add_not_flw_post_to_my_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 3,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_post(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': None,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_none_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 1,
                                                                        'board_id': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_post(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 0,
                                                                        'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_wrong_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 1,
                                                                        'board_id': 0})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_board(self):
        response = self.client.post("/social/addnewposttoboard/", data={'post_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_no_post(self):
        response = self.client.post("/social/addnewposttoboard/", data={'board_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
