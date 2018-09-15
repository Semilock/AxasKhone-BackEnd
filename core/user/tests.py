from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json

from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from rest_framework_simplejwt.settings import api_settings

from core.user.models import Profile


class APIJWTClient(APIClient):
    def login(self, url=reverse("login"), get_response=False, token="access", auth_header_type=0, **credentials):

        auth_header_type = auth_header_type if auth_header_type < len(api_settings.AUTH_HEADER_TYPES) else 0
        response = self.post(url, credentials, format='json')
        if response.status_code == status.HTTP_200_OK:
            self.credentials(
                HTTP_AUTHORIZATION="{0} {1}".format(
                    api_settings.AUTH_HEADER_TYPES[auth_header_type] if isinstance(auth_header_type, int) else auth_header_type,
                    response.data[token]))
            return (True, response) if get_response else True
        else:
            return (False, response) if get_response else False


class APIJWTTestCase(APITestCase):
    client_class = APIJWTClient


class RegistrAPIViewTestCase(APIJWTTestCase):
    url = reverse("register")

    def test_invalid_password(self):
        """
        Test to verify that a post call with invalid passwords
        """
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "password",
            "fullname" : "fullname",
            "bio" : "my bio"
            # "image" : ""
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(400, response.status_code)

    def test_user_registration(self):
        """
        Test to verify that a post call with user valid data
        """
        user_data = {
        "username": "testuser",
        "email": "test@testuser.com",
        "password": "long and hard password!",
        "fullname" : "fullname",
        "bio" : "my bio"
        }
        response = self.client.post(self.url, user_data)
        self.assertEqual(200, response.status_code)

    def test_unique_username_validation(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "long and hard password!",
            "fullname" : "fullname",
            "bio" : "my bio"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(200,response.status_code)

        user_data_2 = {
            "username": "testuser",
            "email": "test2@testuser.com",
            "password": "long and hard password!",
            "fullname" : "fullname",
            "bio" : "my bio"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)

    def test_unique_email_validationon(self):
        """
        Test to verify that a post call with already exists username
        """
        user_data_1 = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "long and hard password!",
            "fullname" : "fullname",
            "bio" : "my bio"
        }
        response = self.client.post(self.url, user_data_1)
        self.assertEqual(200,response.status_code)

        user_data_2 = {
            "username": "testuser2",
            "email": "test@testuser.com",
            "password": "long and hard password!",
            "fullname" : "fullname",
            "bio" : "my bio"
        }
        response = self.client.post(self.url, user_data_2)
        self.assertEqual(400, response.status_code)

class LoginAPIViewTestCase(APIJWTTestCase):
    url = reverse("login")

    def setUp(self):
        self.username = "john@snow.com"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def test_login(self):
        result, response = self.client.login(username=self.username, password=self.password, get_response=True)
        # print (response.content)
        self.assertEqual(True, result)


    def test_authentication_without_password(self):
        response = self.client.post(self.url, {"username": "snowman@gmail.com"})
        self.assertEqual(400, response.status_code)

    def test_authentication_without_username(self):
        response = self.client.post(self.url, {"password": "pass"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_wrong_password(self):
        response = self.client.post(self.url, {"username": self.username, "password": "I_know"})
        self.assertEqual(400, response.status_code)

    def test_authentication_with_valid_data(self):
        response = self.client.post(self.url, {"username": self.username, "password": self.password})
        # print(self.username , self.password)
        self.assertEqual(200, response.status_code)


class ProfileInfoAPIViewTestCase(APIJWTTestCase):
    url = reverse("user:profile_info")

    def setUp(self):
        self.username = "john@snow.com"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.fullname = "john stark"
        self.bio = "my bio"
        self.user = User.objects.create_user(self.username, self.email, self.password)

    def register(self):
        user_data = {
            "username": "testuser",
            "email": "test@testuser.com",
            "password": "long and hard password!",
            "fullname": "fullname",
            "bio": "my bio"
        }
        response = self.client.post(reverse("register"), user_data)
        print(response)

    def test_get_profile(self):
        self.client.login(username=self.username, password=self.password, get_response=True)

        response = self.client.get(self.url)
        self.assertEqual(200, response.status_code)

    # def test_get_another_user_profile(self):
    #     self.client.login(username=self.username, password=self.password, get_response=True)
    #
    #     self.assertEqual(200, response.status_code)

    # def test_edit_profile(self):
    #     self.client.login(username=self.username, password=self.password)
    #     response = self.client.post(self.url, {"email": "test@testuser.com",
    #         "password": "long and hard password!",
    #         "fullname": "fullname",})
    #     self.assertEqual(200, response.status_code)

    # def test_get_profile_info(self):
    #
    #     """
    #         Test to verify profile object bundle
    #     """
    #     response = self.client.get(self.url)
    #     self.assertEqual(200, response.status_code)
    #     print(response.content)
    #
    #     # profile_serializer_data = [ProfileSerializer(instance=self.user.profile).data
    #     # response_data = json.loads(response.content)
    #     # self.assertEqual(profile_serializer_data, response_data)
    #     #
    #     #
    #
    #
    #
    #
    #
    #
    #
