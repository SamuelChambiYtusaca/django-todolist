from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.main.accounts.forms import LoginForm, RegistrationForm

CONST_EXAMPLE_EMAIL = "test@example.com"
CONST_REGISTER = "auth:register"
CONST_LOGIN = "auth:login"

class AccountsTests(TestCase):
    def setUp(self):
        self.register_data = {
            "email": "new@user.com",
            "username": "new_user",
            "password": "test",
            "password_confirmation": "test",
        }
        User.objects.create_user("test", CONST_EXAMPLE_EMAIL, "test")

    def tearDown(self):
        User.objects.get(username="test").delete()

    def test_get_register(self):
        response = self.client.get(reverse(CONST_REGISTER))
        self.assertTemplateUsed(response, "accounts/register.html")
        self.assertIsInstance(response.context["form"], RegistrationForm)

    def test_get_login(self):
        response = self.client.get(reverse(CONST_LOGIN))
        self.assertTemplateUsed(response, "accounts/login.html")
        self.assertIsInstance(response.context["form"], LoginForm)

    def test_register(self):
        response = self.client.post(reverse(CONST_REGISTER), data=self.register_data)
        self.assertRedirects(response, "/auth/login/")
        # new user was created
        self.assertIsNotNone(User.objects.get(username="new_user"))

    def test_login(self):
        # no user is logged in
        self.assertFalse("_auth_user_id" in self.client.session)
        login_data = {"username": "test", "password": "test"}
        response = self.client.post(reverse(CONST_LOGIN), data=login_data)
        self.assertRedirects(response, "/")
        # user is logged in
        self.assertEqual(self.client.session["_auth_user_id"], "1")

    # check if error messages are part of the response
    def test_faulty_login(self):
        # change username for invalid post
        login_data = {"username": 65 * "X", "password": "test"}
        response = self.client.post(reverse(CONST_LOGIN), data=login_data)
        error_message = "Ensure this value has at most 64 characters"
        self.assertContains(response, error_message, status_code=200)

    def test_login_with_non_existent_user(self):
        # change username for invalid post
        login_data = {"username": "notauser", "password": "stillapassowrd"}
        response = self.client.post(reverse(CONST_LOGIN), data=login_data)
        error_message = "Incorrect username and/or password."
        self.assertContains(response, error_message, status_code=200)

    def test_login_with_wrong_password(self):
        # change username for invalid post
        login_data = {"username": "test", "password": "wrongpassword"}
        response = self.client.post(reverse(CONST_LOGIN), data=login_data)
        error_message = "Incorrect username and/or password."
        self.assertContains(response, error_message, status_code=200)

    def test_faulty_register(self):
        # change username for invalid post
        self.register_data["username"] = 65 * "X"
        response = self.client.post(reverse(CONST_REGISTER), data=self.register_data)
        error_message = "Ensure this value has at most 64 characters"
        self.assertContains(response, error_message, status_code=200)

    def test_logout(self):
        response = self.client.get(reverse("auth:logout"))
        self.assertRedirects(response, "/")
        # no user logged in anymore
        self.assertFalse("_auth_user_id" in self.client.session)

