from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class DeleteFollowRequestTest(TestCase):
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

    def create_request(self, user1, user2):
        Request.objects.create(requester=user1, requestee=user2)

    def get_respone(self, data):
        return self.client.post("/social/request/delete/", data)

    def test_public_unrequest(self):
        self.create_request(self.user1, self.user2)
        response = self.get_respone({'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(0, Request.objects.filter(requester=self.user1, requestee=self.user2).count())

    def test_private_unrequest(self):
        self.to_private(self.user2)
        self.create_request(self.user1, self.user2)
        response = self.get_respone({'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_wrong_username(self):
        self.create_request(self.user1, self.user2)
        response = self.get_respone({'username':'test22'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(1, Request.objects.filter(requester=self.user1, requestee=self.user2).count())

    def test_not_requesting_unfollow(self):
        response = self.get_respone({'username':'test2'})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(0, Request.objects.filter(requester=self.user1, requestee=self.user2).count())

    def test_no_username(self):
        self.create_request(self.user1, self.user2)
        response = self.get_respone({})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Request.objects.filter(requester=self.user1, requestee=self.user2).count())
