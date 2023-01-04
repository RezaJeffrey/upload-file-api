from django.db import IntegrityError, transaction
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken

User = get_user_model()


class TestUser(APITestCase):
    """
    Test User model and API Endpoints related to user authentication
    """

    def setUp(self) -> None:
        self.username = "test"
        self.password = "testpassword1234"
        self.email = "test@test.com"
        self.user = User.objects.create_user(
            username=self.username,
            password=self.password,
            email=self.email
        )
        self.access = AccessToken.for_user(self.user)

    def test_user_create_success(self):
        """ test user create using valid credentials"""
        username = "test_username"
        password = "test_password"
        email = "test_email@test.com"
        user = User.objects.create_user(
            username=username,
            password=password,
            email=email
        )
        self.assertEqual(user.username, username)
        self.assertEqual(user.email, email)

    def test_user_password_hash_success(self):
        """ test if password is hashed id db  """
        password = "new_test"
        self.user.set_password(password)
        self.assertNotEqual(self.user.password, password)

    def test_create_user_duplicate_username_failure(self):
        """ test duplicate users in db"""
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                _ = get_user_model().objects.create_user(
                    username=self.username,
                    password=self.password
                )

        count = get_user_model().objects.filter(username=self.username).count()
        self.assertEqual(count, 1)

    def test_set_email_to_user_success(self):
        """ test change or set new email to user """
        email = "new_test@test.com"
        self.user.email = email
        self.user.save()
        self.assertEqual(self.user.email, email)

    def test_set_phone_number_to_user_success(self):
        """ test change or set new phone number to user """
        phone_number = "09201231234"
        self.user.phone_number = phone_number
        self.user.save()
        self.assertEqual(self.user.phone_number, phone_number)

    """ TESTs FOR CHANGE PASSWORD AND PASSWORD VALIDATORS"""
    def test_password_change_success(self):
        url = f"{reverse_lazy('users:users-list')}change_password/"
        payload = {
            "password": "testpassword1234",
            "new_password": "new_new_new",
            "new_password_confirm": "new_new_new"
        }
        access = self.access
        headers = {"Authorization": f'Bearer {str(access)}'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(access))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("message", response.data)

    def test_password_change_short_password_faliure(self):
        url = f"{reverse_lazy('users:users-list')}change_password/"
        payload = {
            "password": "testpassword1234",
            "new_password": "shrt",  # short password
            "new_password_confirm": "shrt"
        }
        access = self.access
        headers = {"Authorization": f'Bearer {str(access)}'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(access))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password_confirm", response.data)
        self.assertIn("new_password", response.data)

    def test_password_change_invalid_password_confirm_faliure(self):
        url = f"{reverse_lazy('users:users-list')}change_password/"
        payload = {
            "password": "testpassword1234",
            "new_password": "newpassword",
            "new_password_confirm": "wrongconfirm"
        }
        access = self.access
        headers = {"Authorization": f'Bearer {str(access)}'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(access))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("new_password", response.data)

    def test_password_change_invalid_current_password_faliure(self):
        url = f"{reverse_lazy('users:users-list')}change_password/"
        payload = {
            "password": "invalid",
            "new_password": "newpassword",
            "new_password_confirm": "newpassword"
        }
        access = self.access
        headers = {"Authorization": f'Bearer {str(access)}'}
        self.client.credentials(HTTP_AUTHORIZATION='Bearer {0}'.format(access))
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    """ ##################### """
    def test_login_valid_credential_success(self):
        """ test user login via correct username and password """
        url = reverse_lazy("users:token_obtain")
        payload = {
            "username": self.username,
            "password": self.password
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("refresh", response.data)
        self.assertIn("access", response.data)

    def test_login_invalid_credential_faliure(self):
        """ test user login using wrong password """
        url = reverse_lazy("users:token_obtain")
        invalid_password = "invalid_password"
        payload = {
            "username": self.username,
            "password": invalid_password
        }
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertNotIn("refresh", response.data)
        self.assertNotIn("access", response.data)

    def test_refresh_token_create_valid_success(self):
        """ test create new access token using refresh token """
        refresh = RefreshToken.for_user(self.user)
        url = reverse_lazy("users:token_refresh")
        payload = {"refresh": str(refresh)}
        response = self.client.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
