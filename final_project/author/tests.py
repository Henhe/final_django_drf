from django.test import TestCase
from author.models import Author, Country
from user.models import User, UserRole
import json
from rest_framework.authtoken.models import Token


class CountryTestCaseAnon(TestCase):
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

    def test_post_country_anon(self):
        data_ = {
            "name": "test",
            "creator": 1,
        }
        response = self.client.post("/api/country/", data_)
        self.assertEqual(response.status_code, 401)

    # def test_auth_user(self):
    #     user_data = {
    #         "username": "test",
    #         "password": "password",
    #     }
    #     response = self.client.post("/api/user/token-auth/", data=user_data)
    #     data = json.loads(response.content)
    #     user = User.objects.filter(username=user_data["username"]).first()
    #     token, _ = Token.objects.get_or_create(user=user)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["data"]["token"], token.key)

    def test_get_countries_list(self):
        response = self.client.get("/api/country/")
        self.assertEqual(response.status_code, 200)

    def test_get_country(self):
        response = self.client.get("/api/country/1/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["name"], "США")

    def test_object_creation(self):
        self.assertEqual(Country.objects.count(), 2)


class CountryTestCase(TestCase):
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
        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key

    def test_post_delete_country(self):
        user = User.objects.filter(username="test").first()
        token, _ = Token.objects.get_or_create(user=user)

        country_data = {
            "name" : "test11",
            "id" :3
        }
        data = json.dumps(country_data)
        response = self.client.post("/api/country/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "test11")

        data = json.dumps(country_data)
        response = self.client.delete("/api/country/3/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_patch_country(self):
        user = User.objects.filter(username="test").first()
        token, _ = Token.objects.get_or_create(user=user)

        country_data = {
            "id": 2,
            "name" : "test_new",
            "creator": user.id
        }
        data = json.dumps(country_data)
        response = self.client.patch("/api/country/2/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "test_new")


class AuthorTestCaseAnon(TestCase):
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

    def test_post_author_anon(self):
        data_ = {
            "name": "Пушкин",
            "country": 2,
            "birth_year": 1799,
            "creator": 1,
        }
        response = self.client.post("/api/country/", data=data_)
        self.assertEqual(response.status_code, 401)

    # def test_auth_user(self):
    #     user_data = {
    #         "username": "test",
    #         "password": "password",
    #     }
    #     response = self.client.post("/api/user/token-auth/", data=user_data)
    #     data = json.loads(response.content)
    #     user = User.objects.filter(username=user_data["username"]).first()
    #     token, _ = Token.objects.get_or_create(user=user)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertEqual(data["data"]["token"], token.key)

    def test_get_authors_list(self):
        response = self.client.get("/api/author/")
        self.assertEqual(response.status_code, 200)

    def test_get_author(self):
        response = self.client.get("/api/author/1/")
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data["name"], "Говард")

    def test_object_creation(self):
        self.assertEqual(Author.objects.count(), 2)


class AuthorTestCase(TestCase):
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

        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key

    def test_post_delete_author(self):
        user = User.objects.filter(username="test").first()
        token, _ = Token.objects.get_or_create(user=user)

        data_ = {
            "name": "Пушкин",
            "country": 2,
            "birth_year": 1799,
            "creator": 1,
            "id": 3
        }
        data = json.dumps(data_)
        response = self.client.post("/api/author/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "Пушкин")

        # data = json.dumps(country_data)
        response = self.client.delete("/api/author/3/",
                                    # data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        self.assertEqual(response.status_code, 204)

    def test_patch_author(self):
        user = User.objects.filter(username="test").first()
        token, _ = Token.objects.get_or_create(user=user)

        country_data = {
            "id": 2,
            "name" : "test_new",
            "creator": user.id,
            "birth_year": 1000,
            "country": 2,
        }
        data = json.dumps(country_data)
        response = self.client.patch("/api/author/2/",
                                    data=data,
                                    HTTP_AUTHORIZATION=f"Token {token}",
                                    content_type="application/json")
        data = json.loads(response.content)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["name"], "test_new")
