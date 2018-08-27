import io
from django.test import TestCase
from authentication.models import User
from PIL import Image
from rest_framework import status
from random import  choice
from string import ascii_letters

class PostTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(email='t@t.com', username='test', password='')
        password = 'sjkkensks'
        self.user.set_password(password)
        self.user.save()
        self.client.login(email=self.user.email, password=password)

    def generate_photo_file(self, height, width):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(height, width), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file

    def test_true_new_post(self):
        data = {
            'picture': self.generate_photo_file(100, 100),
            'caption': '1'
        }

        response = self.client.post("/social/create-new-post/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_big_caption(self):
        data = {
            'picture': self.generate_photo_file(100, 100),
            'caption': ''.join(choice(ascii_letters) for _ in range(2000))
        }
        response = self.client.post("/social/create-new-post/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_big_image(self):
        data = {
            'picture': self.generate_photo_file(4000, 4000),
            'caption': '1'
        }

        response = self.client.post("/social/create-new-post/", data, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)