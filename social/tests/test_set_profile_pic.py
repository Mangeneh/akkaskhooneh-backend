import io
from django.test import TestCase
from authentication.models import User
from PIL import Image
from rest_framework import status

class SetProfileTest(TestCase):
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

    def test_true_set_pic(self):
        pic = self.generate_photo_file(100, 100)
        response = self.client.post("/social/change-pic/", data={'profile_picture':pic}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_big_image(self):
        pic = self.generate_photo_file(4000, 4000)
        response = self.client.post("/social/change-pic/", data={'profile_picture':pic}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_null_image(self):
        response = self.client.post("/social/change-pic/", data={}, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)