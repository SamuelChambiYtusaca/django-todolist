from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

CONST_SAMPLE_MAIL = "test@example.com"

class TodoListTests(APITestCase):
    def setUp(self):
        User.objects.create_user("test", CONST_SAMPLE_MAIL, "test")
        self.client.login(username="test", password="test")
        self.test_data = {"title": "some other title", "todos": []}

    def tearDown(self):
        User.objects.get(username="test").delete()
        self.client.logout()

    def post_new_todolist(self, data):
        url = reverse("api:todolist-list")
        return self.client.post(url, data, format="json")

    def test_create_todolist(self):
        response = self.post_new_todolist(self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], self.test_data["title"])

    def test_get_todolist(self):
        # add todolist
        post_response = self.post_new_todolist(self.test_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        # get todolist
        todolist_id = post_response.data["id"]
        self.assertEqual(todolist_id, 1)
        get_response = self.client.get(f"/api/todolists/{todolist_id}/")
        self.assertEqual(get_response.status_code, status.HTTP_200_OK)
        # check todolist
        self.assertEqual(get_response.data, post_response.data)

    def test_get_when_not_logged_in(self):
        # add some data
        post_response = self.post_new_todolist(self.test_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        # make sure the user is logged out
        self.client.logout()
        response = self.client.get("/api/todolists/1/")
        # expect 200, because reading is allowed for everybody
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_non_existent_todolist(self):
        response = self.client.get("/api/todolists/0/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_post_for_anon_users(self):
        # make sure the user is logged out
        self.client.logout()
        # try posting a todolist
        response = self.post_new_todolist(self.test_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_put_todolist(self):
        # add todolist
        post_response = self.post_new_todolist(self.test_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        # put todolist
        todolist_id = post_response.data["id"]
        put_data = post_response.data
        put_data["title"] = "changed title"
        put_response = self.client.put(
            f"/api/todolists/{todolist_id}/", put_data, format="json"
        )
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        get_response = self.client.get(f"/api/todolists/{todolist_id}/")
        self.assertEqual(put_response.status_code, status.HTTP_200_OK)
        self.assertEqual(get_response.data["title"], "changed title")

    def test_delete_todolist(self):
        # add todolist
        post_response = self.post_new_todolist(self.test_data)
        self.assertEqual(post_response.status_code, status.HTTP_201_CREATED)
        # delete todolist
        todolist_id = post_response.data["id"]
        delete_response = self.client.delete(f"/api/todolists/{todolist_id}/")
        self.assertEqual(delete_response.status_code, status.HTTP_204_NO_CONTENT)
        # get todolist and expect 404
        get_response = self.client.get(f"/api/todolists/{todolist_id}/")
        self.assertEqual(get_response.status_code, status.HTTP_404_NOT_FOUND)

