from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from user.service import UserService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.permissions import UserPermission, ContactPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from user.filters import UserFilterSet
from django.db.models import Q
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from user.serializers import UserLoginSerializer, TokenAuthResponseSerializer
from settings.serializers import ErrorSerializer, DetailSerializer
from settings.views import CustomModelViewSet, CustomAPIView


class UserViewSet(CustomModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserPermission]
    search_fields = ("first_name", "last_name", "username", "email")
    filter_backends = (SearchFilter, OrderingFilter, DjangoFilterBackend)
    ordering = ("-id", )
    ordering_fields = ("id", "role", "email", "username", "is_active")
    filterset_class = UserFilterSet


class TokenAuthView(CustomAPIView):
    permission_classes = [AllowAny]
    request_serializer = UserLoginSerializer
    response_serializer = TokenAuthResponseSerializer
    tags = ["users"]

    # @swagger_auto_schema(
    #     request_body=UserLoginSerializer(),
    #     responses={
    #         status.HTTP_200_OK: TokenAuthResponseSerializer(),
    #         status.HTTP_400_BAD_REQUEST: ErrorSerializer(),
    #         status.HTTP_404_NOT_FOUND: ErrorSerializer(),
    #     },
    #     tags=["users"]
    # )
    def post(self, request):
        user_srv = UserService(request)

        self.data = user_srv.authenticate_user(request.data)

        return self.response()


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_srv = UserService(request)

        data = user_srv.register(request.data)

        return Response(data, status=status.HTTP_201_CREATED)


# class UserActivationView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         uuid = request.GET.get("uuid")
#         token = request.GET.get("token")
#
#         srv = UserService(request)
#
#         user = srv.activate_user(uuid, token)
#
#         return Response({"detail": "User successfully activated"}, status=status.HTTP_200_OK)


# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         srv = UserService(request)
#
#         srv.reset_password(request.data)
#
#         return Response(
#             {"detail": "Email with password reset link sent to your email"},
#             status=status.HTTP_200_OK
#         )
#
#
# class ConfirmPasswordReset(APIView):
#     permission_classes = [AllowAny]
#
#     def post(self, request):
#         uuid = request.GET.get("uuid")
#         token = request.GET.get("token")
#
#         srv = UserService(request)
#
#         srv.confirm_password_reset(uuid, token, request.data)
#
#         return Response({"detail": "Password successfully reset"}, status=status.HTTP_200_OK)
#
#
# class EditPasswordView(APIView):
#
#     def put(self, request):
#         srv = UserService(request)
#
#         srv.edit_password(request.data)
#
#         return Response({"detail": "Password successfully updated"}, status.HTTP_200_OK)
