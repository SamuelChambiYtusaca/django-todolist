from django.test import TestCase

from src.main.lists.forms import TodoListForm

CONST_REQUIRED = "This field is required."

class TodoListFormTests(TestCase):
    def setUp(self):
        self.vaild_form_data = {"title": "some title"}
        self.too_long_title = {"title": 129 * "X"}

    def test_valid_input(self):
        form = TodoListForm(self.vaild_form_data)
        self.assertTrue(form.is_valid())

    def test_no_title(self):
        form = TodoListForm({})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"title": [CONST_REQUIRED]})

    def test_empty_title(self):
        form = TodoListForm({"title": ""})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {"title": [CONST_REQUIRED]})

    def test_too_long_title(self):
        form = TodoListForm(self.too_long_title)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors,
            {
                "title": [
                    "Ensure this value has at most 128 " + "characters (it has 129)."
                ]
            },
        )
