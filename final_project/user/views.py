from user.models import User
from user.serializers import UserSerializer
from rest_framework.views import APIView
from user.service import UserService
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.permissions import UserPermission
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from user.filters import UserFilterSet
from user.serializers import UserLoginSerializer, TokenAuthResponseSerializer
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



