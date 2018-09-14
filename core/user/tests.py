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

        # self.assertEqual(response.data['user_data'], self.username)
