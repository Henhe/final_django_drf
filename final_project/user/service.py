from settings.service import BaseService
from user.serializers import UserLoginSerializer, RegisterSerializer, \
    UserSerializer, UserEmailSerializer, PasswordResetSerializer, PasswordEditSerializer
from django.contrib.auth import authenticate
from django.http.response import HttpResponseBadRequest
from rest_framework.authtoken.models import Token
from user.models import  User
from django.db import IntegrityError
from settings.exceptions import Exception404, Exception400
from user.constants import UserErrorMessage
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from user.helpers import account_activation_token, password_reset_token
# from user.tasks import send_confirmation_email_task


class UserService(BaseService):

    def authenticate_user(self, user_data: dict):
        serializer = UserLoginSerializer(data=user_data)
        # print(serializer.initial_data)
        user = authenticate(
            username=serializer.initial_data.get("username"),
            password=serializer.initial_data.get("password"),
        )

        if not user:
            return {"error": "Invalid password or username"}

        token, _ = Token.objects.get_or_create(user=user)

        return {"token": token.key}

    def register(self, user_data: dict):
        serializer = RegisterSerializer(data=user_data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        user.is_active = True
        user.save()
        # self.send_confirmation_email(user)
        # send_confirmation_email_task.delay(
        #     user.pk,
        #     get_current_site(self._request).domain,
        #     account_activation_token.make_token(user)
        # )

        return UserSerializer(user).data

    # def send_confirmation_email(self, user):
    #     print(f"http://{get_current_site(self._request).domain}/api/activate?uuid={ urlsafe_base64_encode(force_bytes(user.pk)) }&token={ account_activation_token.make_token(user) }")
    #     message = render_to_string(
    #         "confirm_email.html",
    #         {
    #             "domain": get_current_site(self._request).domain,
    #             "uuid": urlsafe_base64_encode(force_bytes(user.pk)),
    #             "token": account_activation_token.make_token(user),
    #         }
    #     )
    #     EmailMessage("Email confirmation", message, to=[user.email]).send()


    # def activate_user(self, uuid, token):
    #     if not uuid or not token:
    #         raise Exception400(UserErrorMessage.ACTIVATION_FAILED.value)
    #
    #     user_id = force_str(urlsafe_base64_decode(uuid))
    #     user = User.objects.filter(pk=user_id).first()
    #
    #     if user and account_activation_token.check_token(user, token):
    #         user.is_active = True
    #         user.save()
    #         return user
    #
    #     raise Exception400(UserErrorMessage.ACTIVATION_FAILED.value)
    #
    #
    # # def reset_password(self, user_data):
    #     serializer = UserEmailSerializer(data=user_data)
    #
    #     serializer.is_valid(raise_exception=True)
    #     email = serializer.data.get("email")
    #     user = User.objects.filter(email=email).first()
    #
    #     if not user:
    #         raise Exception400(UserErrorMessage.NOT_FOUND)
    #
    #     self.send_reset_password_email(user)

    # def send_reset_password_email(self, user):
    #     print(f"http://{get_current_site(self._request).domain}/api/confirm-password-reset/?uuid={ urlsafe_base64_encode(force_bytes(user.pk)) }&token={ password_reset_token.make_token(user) }")
    #     message = render_to_string(
    #         "reset_password.html",
    #         {
    #             "domain": get_current_site(self._request).domain,
    #             "uuid": urlsafe_base64_encode(force_bytes(user.pk)),
    #             "token": password_reset_token.make_token(user),
    #         }
    #     )
    #     # EmailMessage("Email confirmation", message, to=[user.email]).send()

    # def confirm_password_reset(self, uuid, token, user_data):
    #     if not uuid or not token:
    #         raise Exception400(UserErrorMessage.PASSWORD_RESET_FAILED.value)
    #
    #     user_id = force_str(urlsafe_base64_decode(uuid))
    #     user = User.objects.filter(pk=user_id).first()
    #
    #     if user and password_reset_token.check_token(user, token):
    #         serializer = PasswordResetSerializer(data=user_data)
    #         serializer.is_valid(raise_exception=True)
    #         new_password = serializer.data.get("new_password")
    #         user.set_password(new_password)
    #         user.save()
    #         return user
    #
    #     raise Exception400(UserErrorMessage.PASSWORD_RESET_FAILED.value)
    #
    # def edit_password(self, user_data):
    #     serializer = PasswordEditSerializer(data=user_data)
    #     serializer.is_valid(raise_exception=True)
    #
    #     if not self._user.check_password(serializer.data.get("old_password")):
    #         raise Exception400(UserErrorMessage.WRONG_PASSWORD.value)
    #
    #     self._user.set_password(serializer.data.get("new_password"))
    #     self._user.save()
