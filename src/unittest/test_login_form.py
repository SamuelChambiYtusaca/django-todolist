from django import forms
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from src.main.accounts.forms import LoginForm, RegistrationForm

CONST_EXAMPLE_EMAIL = "test@example.com"
CONST_REQUIRED = "This field is required."

class LoginFormTests(TestCase):

    # valid test case is covered by AccountsTests (because we need a user)
    def setUp(self):
        self.too_long_password = {"username": "test", "password": 65 * "X"}
        self.too_long_username = {"username": 65 * "X", "password": "test"}

    def test_too_long_username(self):
        form = LoginForm(self.too_long_username)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "username": [
                    "Ensure this value has at most 64" + " characters (it has 65)."
                ]
            },
        )

    def test_too_long_password(self):
        form = LoginForm(self.too_long_password)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "password": [
                    "Ensure this value has at most 64" + " characters (it has 65)."
                ]
            },
        )

    def test_no_username(self):
        form = LoginForm({"password": "test"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"username": [CONST_REQUIRED]})

    def test_no_password(self):
        form = LoginForm({"username": "test"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"password": [CONST_REQUIRED]})

    def test_empty_username(self):
        form = LoginForm({"username": "", "password": "test"})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"username": [CONST_REQUIRED]})

    def test_empty_password(self):
        form = LoginForm({"username": "test", "password": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"password": [CONST_REQUIRED]})


class RegistrationFormTests(TestCase):
    def setUp(self):
        self.valid_form_data = {
            "email": CONST_EXAMPLE_EMAIL,
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        }
        self.invalid_email = {
            "email": "test(at)example.com",
            "username": "test",
            "password": "test",
            "password_confirmation": "test",
        }
        self.non_matching_passwords = {
            "email": CONST_EXAMPLE_EMAIL,
            "username": "test",
            "password": "test1",
            "password_confirmation": "test2",
        }

    # some tests can be skipped because of the coverage of LoginFormTests
    def test_valid_input(self):
        form = RegistrationForm(self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_email(self):
        form = RegistrationForm(self.invalid_email)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"email": ["Enter a valid email address."]})

    def test_non_matching_passwords(self):
        form = RegistrationForm(self.non_matching_passwords)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"__all__": ["Passwords don't match."]})
