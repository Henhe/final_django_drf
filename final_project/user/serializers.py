from rest_framework.serializers import ModelSerializer, IntegerField, CharField, EmailField, Serializer
from user.models import User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ["password", "contacts"]


class UserLoginSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password"]


class RegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data: dict):
        user = User.objects.create_user(**validated_data)
        return user


class UserEmailSerializer(Serializer):
    email = EmailField(required=True)


class PasswordResetSerializer(Serializer):
    new_password = CharField(required=True, min_length=8)


class PasswordEditSerializer(PasswordResetSerializer):
    old_password = CharField(required=True)


class TokenSerializer(Serializer):
    token = CharField(read_only=True)


class TokenAuthResponseSerializer(Serializer):
    data = TokenSerializer()
