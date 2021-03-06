from django.core.exceptions import ObjectDoesNotExist

from django.test import TestCase
from rest_framework import status
from authentication.models import User
from social.models import Board, Followers, Posts, BoardContains


class DeletePostFromBoardTest(TestCase):

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

        self.board1 = Board.objects.create(owner=self.user1, name='b1')
        self.board2 = Board.objects.create(owner=self.user2, name='b2')

        self.post1 = Posts.objects.create(owner=self.user1, picture="1.png")
        self.board_c = BoardContains.objects.create(board=self.board1, post=self.post1)
        self.board_c = BoardContains.objects.create(board=self.board2, post=self.post1)

        self.flw = Followers.objects.create(user=self.user1, following=self.user2)

        self.client.login(email="t1@t1@.com", password="yhes11")

    def test_delete_true_post(self):
        response = self.client.post("/social/deletepostfromboard/", data={'board_id': 1,
                                                                          'post_id': 1})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        try:
            BoardContains.objects.get(board_id=1, post_id=1)
            self.assertFalse(True, "post not deleted!")
        except ObjectDoesNotExist as e:
            pass

    def test_delete_other_board(self):
        response = self.client.post("/social/deletepostfromboard/", data={'board_id': 2,
                                                                          'post_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        try:
            BoardContains.objects.get(board_id=2, post_id=1)
        except ObjectDoesNotExist as e:
            self.assertFalse(True, "post deleted!")

    def test_delete_no_board(self):
        response = self.client.post("/social/deletepostfromboard/", data={'board_id': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_no_post(self):
        response = self.client.post("/social/deletepostfromboard/", data={'post_id': None})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_no_board_no_data(self):
        response = self.client.post("/social/deleteboard/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_random_board(self):
        response = self.client.post("/social/deleteboard/", data={'board_id': 3, 'post_id': 1})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
