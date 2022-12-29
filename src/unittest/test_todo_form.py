from django.test import TestCase

from src.main.lists.forms import TodoForm

CONST_REQUIRED = "This field is required."

class TodoFormTests(TestCase):
    def setUp(self):
        self.valid_form_data = {"description": "something to be done"}
        self.too_long_description = {"description": 129 * "X"}

    def test_valid_input(self):
        form = TodoForm(self.valid_form_data)
        self.assertTrue(form.is_valid())

    def test_no_description(self):
        form = TodoForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"description": [CONST_REQUIRED]})

    def test_empty_description(self):
        form = TodoForm({"description": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"description": [CONST_REQUIRED]})

    def test_too_title(self):
        form = TodoForm(self.too_long_description)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "description": [
                    "Ensure this value has at most 128 " + "characters (it has 129)."
                ]
            },
        )
