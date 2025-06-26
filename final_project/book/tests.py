from django.test import TestCase
from book.models import Book, BookAuthor, RaitingBook, FavoriteBookцыд
from user.models import User, UserRole
from author.models import Author, Country
from genre.models import Genre
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
        country1 = Country.objects.create(id=1, name="США", creator=user)
        country2 = Country.objects.create(id=2, name="РФ", creator=user)
        author1 = Author.objects.create(id=1, name='Говард', country=country1, creator=user, birth_year=1900)
        author2 = Author.objects.create(id=2, name='Горький', country=country2, creator=user, birth_year=1870)
        genre1 = Genre.objects.create(id=1, name="фэнтези", creator=user)
        genre2 = Genre.objects.create(id=2, name="история", creator=user)

        book1 = Book.objects.create(id=1, isbn="1234567890123", name="Конан Варвар", genre=genre1, creator=user)
        book2 = Book.objects.create(id=2, isbn="1234567890122",name="Детство", genre=genre2,  creator=user)

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


class BookTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()
        country1 = Country.objects.create(id=1, name="США", creator=user)
        country2 = Country.objects.create(id=2, name="РФ", creator=user)
        author1 = Author.objects.create(id=1, name='Говард', country=country1, creator=user, birth_year=1900)
        author2 = Author.objects.create(id=2, name='Горький', country=country2, creator=user, birth_year=1870)
        genre1 = Genre.objects.create(id=1, name="фэнтези", creator=user)
        genre2 = Genre.objects.create(id=2, name="история", creator=user)

        book1 = Book.objects.create(id=1, isbn="1234567890123", name="Конан Варвар", genre=genre1, creator=user)
        book2 = Book.objects.create(id=2, isbn="1234567890122", name="Детство", genre=genre2, creator=user)
        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key

    def test_post_delete_book(self):
        user = User.objects.filter(username="test").first()
        genre = Genre.objects.filter(name="фэнтези").first()
        author1 = Author.objects.filter(name="Говард").first()
        token, _ = Token.objects.get_or_create(user=user)

        data_ = {
            "isbn" : "1234567890121",
            "name" : "test11",
            "id" :3,
            "genre" : genre.id,
            "authors": [author1.id],
        }
        data = json.dumps(data_)
        response = self.client.post("/api/book/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "test11")

        response = self.client.delete("/api/book/3/",
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_patch_book(self):
        user = User.objects.filter(username="test").first()
        genre = Genre.objects.filter(name="фэнтези").first()
        author1 = Author.objects.filter(name="Говард").first()
        author2 = Author.objects.filter(name="Горький").first()
        token, _ = Token.objects.get_or_create(user=user)

        data_ = {
            "id": 2,
            "name" : "test_new",
            "isbn" : "1234567890120",
            "genre" : genre.id,
            "authors": [author1.id, author1.id],
            "creator": user.id,
        }
        data = json.dumps(data_)
        response = self.client.patch("/api/book/2/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "test_new")
        self.assertEqual(BookAuthor.objects.filter(book__id=2).count(), 2)

class RaitingBookTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()

        country1 = Country.objects.create(id=1, name="США", creator=user)
        country2 = Country.objects.create(id=2, name="РФ", creator=user)
        author1 = Author.objects.create(id=1, name='Говард', country=country1, creator=user, birth_year=1900)
        author2 = Author.objects.create(id=2, name='Горький', country=country2, creator=user, birth_year=1870)
        genre1 = Genre.objects.create(id=1, name="фэнтези", creator=user)
        genre2 = Genre.objects.create(id=2, name="история", creator=user)

        book1 = Book.objects.create(id=1, isbn="1234567890123", name="Конан Варвар", genre=genre1, creator=user)
        book2 = Book.objects.create(id=2, isbn="1234567890122", name="Детство", genre=genre2, creator=user)
        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key

    def test_get_raitingbooks_list(self):
        response = self.client.get("/api/book/raiting/")
        self.assertEqual(response.status_code, 200)

    def test_post_raitingbook(self):
        user = User.objects.filter(username="test").first()
        book = Book.objects.filter(isbn="1234567890123").first()
        token, _ = Token.objects.get_or_create(user=user)

        data_ = {
            "id" :1,
            "creator":user.id,
            "raiting":8,
        }
        data = json.dumps(data_)
        response = self.client.post(f"/api/book/raiting/{book.id}/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["raiting"], 8)
        self.assertEqual(RaitingBook.objects.all().count(), 1)
        # повторная отправка перезаписывает
        data_ = {
            "id": 1,
            "creator": user.id,
            "raiting": 6,
        }
        data = json.dumps(data_)
        response = self.client.post(f"/api/book/raiting/{book.id}/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["raiting"], 6)
        self.assertEqual(RaitingBook.objects.all().count(), 1)

class FavoriteBookTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()

        country1 = Country.objects.create(id=1, name="США", creator=user)
        country2 = Country.objects.create(id=2, name="РФ", creator=user)
        author1 = Author.objects.create(id=1, name='Говард', country=country1, creator=user, birth_year=1900)
        author2 = Author.objects.create(id=2, name='Горький', country=country2, creator=user, birth_year=1870)
        genre1 = Genre.objects.create(id=1, name="фэнтези", creator=user)
        genre2 = Genre.objects.create(id=2, name="история", creator=user)

        book1 = Book.objects.create(id=1, isbn="1234567890123", name="Конан Варвар", genre=genre1, creator=user)
        book2 = Book.objects.create(id=2, isbn="1234567890122", name="Детство", genre=genre2, creator=user)
        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key

    def test_get_favoritebooks_list(self):
        response = self.client.get("/api/book/raiting/")
        self.assertEqual(response.status_code, 200)

    def test_post_delete_favoritebook(self):
        user = User.objects.filter(username="test").first()
        book = Book.objects.filter(isbn="1234567890123").first()
        book1 = Book.objects.filter(isbn="1234567890122").first()
        token, _ = Token.objects.get_or_create(user=user)

        data_ = {
            "id" :1,
            "user":user.id,
            "book":book.id
        }
        data = json.dumps(data_)
        response = self.client.post(f"/api/book/favorite/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)

        data_ = {
            "id": 2,
            "user": user.id,
            "book": book.id
        }
        data = json.dumps(data_)
        response = self.client.post(f"/api/book/favorite/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")

        self.assertEqual(response.status_code, 400)

        data_ = {
            "id": 3,
            "user": user.id,
            "book": book1.id
        }
        data = json.dumps(data_)
        response = self.client.post(f"/api/book/favorite/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(FavoriteBook.objects.filter(user__id=user.id).count(), 2)

        data_ = {
            "book": book1.id,
            "user": user.id,
        }
        data = json.dumps(data_)
        response = self.client.delete(f"/api/book/favorite/",
                                      data=data,
                                      HTTP_AUTHORIZATION=f"Token {token}",
                                      content_type="application/json")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(FavoriteBook.objects.filter(user__id=user.id).count(), 1)

