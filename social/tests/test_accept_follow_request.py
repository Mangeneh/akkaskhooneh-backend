from django.test import TestCase
from authentication.models import User
from social.models import Posts, Followers, Request
from rest_framework import status

class AcceptRequestTest(TestCase):
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

    def test_true_accept(self):
        request = Request.objects.create(requester=self.user2, requestee=self.user1)
        response = self.client.post("/social/request/accept/", data={'request_id': request.id, 'accept': True}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(0, Request.objects.filter(requester=self.user2, requestee=self.user1).count())
        self.assertEqual(1, Followers.objects.filter(user=self.user2, following=self.user1).count())

    def test_true_reject(self):
        request = Request.objects.create(requester=self.user2, requestee=self.user1)
        response = self.client.post("/social/request/accept/", data={'request_id': request.id, 'accept': False}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(0, Request.objects.filter(requester=self.user2, requestee=self.user1).count())
        self.assertEqual(0, Followers.objects.filter(user=self.user2, following=self.user1).count())

    def test_other_person_accept(self):
        request = Request.objects.create(requester=self.user1, requestee=self.user2)
        response = self.client.post("/social/request/accept/", data={'request_id': request.id, 'accept': True}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(0, Request.objects.filter(requester=self.user2, requestee=self.user1).count())
        self.assertEqual(0, Followers.objects.filter(user=self.user2, following=self.user1).count())

    def test_wrong_request_id_accept(self):
        request = Request.objects.create(requester=self.user2, requestee=self.user1)
        response = self.client.post("/social/request/accept/", data={'request_id': 392891, 'accept': True}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Request.objects.filter(requester=self.user2, requestee=self.user1).count())
        self.assertEqual(0, Followers.objects.filter(user=self.user2, following=self.user1).count())

    def test_no_request_id_accept(self):
        request = Request.objects.create(requester=self.user2, requestee=self.user1)
        response = self.client.post("/social/request/accept/", data={'accept': True}, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(1, Request.objects.filter(requester=self.user2, requestee=self.user1).count())
        self.assertEqual(0, Followers.objects.filter(user=self.user2, following=self.user1).count())
