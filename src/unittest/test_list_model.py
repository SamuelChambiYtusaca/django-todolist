from django.contrib.auth.models import User
from django.test import TestCase

from src.main.lists.models import Todo, TodoList

class ListModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("test", "test@example.com", "test")
        self.todolist = TodoList(title="title", creator=self.user)
        self.todolist.save()
        self.todo = Todo(
            description="description", todolist_id=self.todolist.id, creator=self.user
        )
        self.todo.save()

    def tearDown(self):
        self.todo.delete()
        self.todolist.delete()
        self.user.delete()

    def test_count_todos(self):
        self.assertEqual(self.todolist.count(), 1)
        new_todo = Todo(
            description="test", todolist_id=self.todolist.id, creator=self.user
        )
        new_todo.save()
        self.assertEqual(self.todolist.count(), 2)

    def test_count_open_todos(self):
        self.assertEqual(self.todolist.count_open(), 1)
        new_todo = Todo(
            description="test", todolist_id=self.todolist.id, creator=self.user
        )
        new_todo.save()
        self.assertEqual(self.todolist.count_open(), 2)
        new_todo.close()
        self.assertEqual(self.todolist.count_open(), 1)

    def test_count_closed_todos(self):
        self.assertEqual(self.todolist.count_finished(), 0)
        new_todo = Todo(
            description="test", todolist_id=self.todolist.id, creator=self.user
        )
        new_todo.close()
        self.todo.close()
        self.assertEqual(self.todolist.count_finished(), 2)
        self.assertIsNotNone(new_todo.finished_at)
        self.todo.reopen()
        self.assertEqual(self.todolist.count_finished(), 1)
        self.assertIsNone(self.todo.finished_at)
