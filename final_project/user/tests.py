from django.test import TestCase
from user.models import User, UserRole
from rest_framework.authtoken.models import Token
import random
import json
from unittest import mock


class AnonUserTestCase(TestCase):
    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            first_name="John",
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()

    def test_get_users_list_as_anon(self):
        response = self.client.get("/api/users/")
        self.assertEqual(response.status_code, 401)

    @mock.patch("user.service.UserService.send_confirmation_email")
    def test_register_user(self, mock_send_email):
        user_data = {
            "email": "test_reg@email.com",
            "username": "new_test",
            "password": "hardpassword@@123",
        }
        response = self.client.post("/api/register/", data=user_data)
        data = json.loads(response.content)
        new_user = User.objects.filter(username=user_data["username"]).first()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["email"], user_data["email"])
        self.assertEqual(data["username"], user_data["username"])
        self.assertEqual(data["isActive"], False)
        mock_send_email.assert_called()
        mock_send_email.assert_called_with(new_user)

    def test_auth_user(self):
        user_data = {
            "username": "test",
            "password": "password",
        }
        response = self.client.post("/api/token-auth/", data=user_data)
        data = json.loads(response.content)
        user = User.objects.filter(username=user_data["username"]).first()
        token, _ = Token.objects.get_or_create(user=user)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["token"], token.key)

    @mock.patch("user.service.UserService.activate_user")
    def test_activate_user(self, activate_user_mock):
        response = self.client.post("/api/activate/?uuid=asd&token=aasdqwe123")
        data = json.loads(response.content)
        # user = User.objects.filter(username=user_data["username"]).first()
        # token, _ = Token.objects.get_or_create(user=user)
        self.assertEqual(response.status_code, 200)
        activate_user_mock.assert_called_with("asd", "aasdqwe123")


class UserTestCase(TestCase):
    # def create_test_users(self, count):
    #     print("Setup users")
    #     for number in range(count):
    #         user = User.objects.create_user(
    #             f"test{number}@test.com",
    #             f"test{number}",
    #             is_active=random.choice([True, False]),
    #             role=random.choice(UserRole.values())
    #         )
    #         user.set_password("password")
    #         user.save()

    def setUp(self) -> None:
        user = User.objects.create_user(
            "test@test.com",
            "test",
            is_active=True,
            first_name="John",
            role=UserRole.ADMIN.value
        )
        user.set_password("password")
        user.save()
        token, _ = Token.objects.get_or_create(user=user)
        self.client.defaults["HTTP_AUTHORIZATION"] = "Token " + token.key
        for number in range(5):
            user = User.objects.create_user(
                f"test{number}@test.com",
                f"test{number}",
                is_active=random.choice([True, False]),
                role=random.choice(UserRole.values())
            )
            user.set_password("password")
            user.save()

    def test_get_users_list_order_by_id(self):
        first_user = User.objects.order_by("id").first()
        response = self.client.get("/api/users/?ordering=id")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["meta"]["count"], 6)
        self.assertEqual(data["meta"]["page"], 1)
        self.assertEqual(data["meta"]["perPage"], 1)
        self.assertEqual(data["data"][0]["id"], first_user.id)

    def test_get_users_list(self):
        last_user = User.objects.order_by("-id").first()
        response = self.client.get("/api/users/")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["meta"]["count"], 6)
        self.assertEqual(data["meta"]["page"], 1)
        self.assertEqual(data["meta"]["perPage"], 1)
        self.assertEqual(data["data"][0]["id"], last_user.id)

    def test_get_users_list_paginated(self):
        response = self.client.get("/api/users/?page=2&perPage=3")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 3)
        self.assertEqual(data["meta"]["count"], 6)
        self.assertEqual(data["meta"]["page"], 2)
        self.assertEqual(data["meta"]["perPage"], 3)

    def test_get_users_list_with_search(self):
        response = self.client.get("/api/users/?search=jo")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), 1)
        self.assertEqual(data["meta"]["count"], 1)
        self.assertEqual(data["meta"]["page"], 1)
        self.assertEqual(data["meta"]["perPage"], 1)
        self.assertEqual(data["data"][0]["firstName"], "John")

    def test_get_users_list_with_role_filter(self):
        admin_count = User.objects.filter(role=UserRole.ADMIN.value).count()
        response = self.client.get(f"/api/users/?role={UserRole.ADMIN.value}&perPage=10")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data["data"]), admin_count)
        self.assertEqual(data["meta"]["count"], admin_count)
        self.assertEqual(data["meta"]["page"], 1)
        self.assertEqual(data["meta"]["perPage"], 10)
