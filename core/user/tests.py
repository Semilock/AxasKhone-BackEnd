from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework.utils import json


class RegistrAPIViewTestCase(APITestCase):
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

class LoginAPIViewTestCase(APITestCase):
    url = reverse("login")

    def setUp(self):
        self.username = "john@snow.com"
        self.email = "john@snow.com"
        self.password = "you_know_nothing"
        self.user = User.objects.create_user(self.username, self.email, self.password)

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
        print(self.username , self.password)
        self.assertEqual(200, response.status_code)

