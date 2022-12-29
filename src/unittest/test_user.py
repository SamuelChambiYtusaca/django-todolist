from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CONST_SAMPLE_MAIL = "test@example.com"

class UserTests(APITestCase):
    def setUp(self):
        User.objects.create_user("test", CONST_SAMPLE_MAIL, "test")
        self.client.login(username="test", password="test")

    def tearDown(self):
        User.objects.get(username="test").delete()
        self.client.logout()

    def test_post_on_read_only(self):
        response = self.client.post("api:user-list", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_user_if_not_admin(self):
        # get user (test user from setup)
        get_response = self.client.get("/api/users/{}/".format(1))
        self.assertEqual(get_response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_user_if_admin(self):
        # create admin user and login as such
        User.objects.create_superuser("admin", "admin@example.com", "admin")
        self.client.login(username="admin", password="admin")
        # get user (test user from setup)
        get_response = self.client.get("/api/users/{}/".format(1))
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        # check user
        self.assertEqual(get_response.data["username"], "test")
