from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from settings.models import Timestamp
from settings.enums import CustomEnum
from django.contrib.auth.models import PermissionsMixin

class UserRole(CustomEnum):
    ADMIN = 1
    LIBRARIAN = 2
    READER = 3


class UserManager(BaseUserManager):
    def create_user(
            self,
            email,
            username,
            password=None,
            first_name="",
            last_name="",
            is_active=False,
            role=UserRole.READER.value,

    ):
        user = self.model(
            email=email,
            first_name=first_name,
            last_name=last_name,
            is_active=is_active,
            username=username,
            role=role,
        )
        user.set_password(password)
        # user.role = UserRole.REGULAR.value
        user.save(using=self._db)
        return user

    def create_superuser(
            self,
            username,
            password=None
    ):
        user = self.create_user(
            email=f'{username}@test.test',
            is_active=True,
            role=UserRole.ADMIN.value,
            username=username,
            password=password,
        )
        user.is_superuser=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin, Timestamp, models.Model):
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=100)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=False)
    role = models.PositiveSmallIntegerField(default=UserRole.READER.value)

    objects = UserManager()
    USERNAME_FIELD = "username"

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.role == UserRole.ADMIN.value


