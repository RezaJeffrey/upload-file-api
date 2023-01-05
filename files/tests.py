from django.urls import reverse_lazy
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from files.models import File
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile
import shutil


User = get_user_model()


class FileTest(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            username="test",
            password="testpassword"
        )
        self.title = "test_title"
        self.file = SimpleUploadedFile(

            "best_file_eva.txt",
            b"these are the file contents!"
        )
        File.objects.create(
            user=self.user,
            title=self.title,
            file=self.file
        )

    def test_file_create(self):
        file = File.objects.create(
            user=self.user,
            title=self.title,
            file=self.file
        )
        self.assertEqual(file.user.username, self.user.username)
        self.assertEqual(file.title, self.title)

    def test_file_create_view_success(self):
        url = reverse_lazy('files:files-list')
        uploaded_file = SimpleUploadedFile('test_file.txt', b'this is test file')
        payload = {
            "title": "test_username",
            "file": uploaded_file
        }
        access = AccessToken.for_user(self.user)  # Normal user
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(access))
        response = self.client.post(url, payload)
        self.assertIn("title", response.data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        shutil.rmtree('media/user_test', ignore_errors=True)

    def test_file_create_view_invalid_credentials_faliure(self):
        url = reverse_lazy('files:files-list')
        uploaded_file = SimpleUploadedFile('test_file.txt', b'this is test file')
        payload = {
            "title": "test_username",
            "file": uploaded_file
        }
        response = self.client.post(url, payload)
        self.assertEqual(status.HTTP_401_UNAUTHORIZED, response.status_code)
        self.assertIn("detail", response.data)
