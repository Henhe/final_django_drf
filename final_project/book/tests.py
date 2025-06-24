from django.test import TestCase
from book.models import Book
from user.models import User, UserRole
import json
from rest_framework.authtoken.models import Token


class BookTestCaseAnon(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()
        book1 = Book.objects.create(id=1, name="фэнтези", creator=user)
        book2 = Book.objects.create(id=2, name="история", creator=user)

    def test_post_book_anon(self):
        data_ = {
            "name": "test",
            "creator": 1,
        }
        response = self.client.post("/api/genre/", data_)
        self.assertEqual(response.status_code, 401)

    def test_get_books_list(self):
        response = self.client.get("/api/genre/")
        self.assertEqual(response.status_code, 200)

    def test_get_book(self):
        response = self.client.get("/api/genre/1/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["name"], "фэнтези")

    def test_object_creation(self):
        self.assertEqual(Book.objects.count(), 2)


# class BookTestCase(TestCase):
#     def setUp(self) -> None:
#         user = User.objects.create_user(
#             "test@test.com",
#             "test",
#             is_active=True,
#             role=UserRole.ADMIN.value
#         )
#         user.set_password("password")
#         user.save()
#         genre1 = Genre.objects.create(id=1, name="фэнтези", creator=user)
#         genre2 = Genre.objects.create(id=2, name="история", creator=user)
#         token, _ = Token.objects.get_or_create(user=user)
#         self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key
#
#     def test_post_delete_book(self):
#         user = User.objects.filter(username="test").first()
#         token, _ = Token.objects.get_or_create(user=user)
#
#         data_ = {
#             "name" : "test11",
#             "id" :3
#         }
#         data = json.dumps(data_)
#         response = self.client.post("/api/book/",
#                                     data=data,
#                                     HTTP_AUTHORIZATION=f"Token {token}",
#                                     content_type="application/json")
#         data = json.loads(response.content)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(data["name"], "test11")
#
#         response = self.client.delete("/api/book/3/",
#                                     HTTP_AUTHORIZATION=f"Token {token}",
#                                     content_type="application/json")
#         self.assertEqual(response.status_code, 204)
#
#
#     def test_patch_genre(self):
#         user = User.objects.filter(username="test").first()
#         token, _ = Token.objects.get_or_create(user=user)
#
#         country_data = {
#             "id": 2,
#             "name" : "test_new",
#             "creator": user.id
#         }
#         data = json.dumps(country_data)
#         response = self.client.patch("/api/book/2/",
#                                     data=data,
#                                     HTTP_AUTHORIZATION=f"Token {token}",
#                                     content_type="application/json")
#         data = json.loads(response.content)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(data["name"], "test_new")

