from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Board
from rest_framework import status

class FeedTest(TestCase):
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
        self.board = Board.objects.create(owner=self.user2, name='test')

    def test_can_see_public_user_board(self):
        response = self.client.get("/social/boardsdetails/"+str(self.board.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_can_see_private_user_board(self):
        self.user2.is_private = True
        self.user2.save()
        response = self.client.get("/social/boardsdetails/"+str(self.board.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_see_my_board(self):
        board = Board.objects.create(owner=self.user1, name='test')
        response = self.client.get("/social/boardsdetails/"+str(board.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_can_see_my_private_board(self):
        self.user1.is_private = True
        self.user1.save()
        board = Board.objects.create(owner=self.user1, name='test')
        response = self.client.get("/social/boardsdetails/"+str(board.id)+"/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)

    def test_bad_board_id(self):
        response = self.client.get("/social/boardsdetails/232919/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
